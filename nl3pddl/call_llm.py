
import json
import os
import copy
import logging
from typing import Any, List, Optional, Dict
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from pddl.core import Domain, Action
from pddl.parser.domain import DomainParser
from pddl.formatter import domain_to_string

from nl3pddl.params import MODELS, Params
from nl3pddl.dataset import Dataset, PipelineResult
import re


load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")

if not os.getenv("DEEPSEEK_API_KEY"):
    raise ValueError("DEEPSEEK_API_KEY environment variable not set. Please set it in your .env file.")


DOMAIN_PARSER = DomainParser()

def matching_closing_paren(s : str) -> int:
    """ Returns the index of the closing ) for the ( at the first pos """
    assert s[0] == '('
    count = 1
    i = 1
    while i < len(s):
        if s[i] == ')':
            count -= 1
        elif s[i] == '(':
            count += 1
        if count == 0:
            return i
        i += 1
    return None

def action_syntax_check(model_output : str) -> str | PipelineResult:
    """
    Returns an error if the model outputs invalid PDDL, otherwise returns
    the string of the correct PDDL extracted from the model output
    """
    start_index : int = model_output.find("(")
    model_output : str = model_output[start_index:]
    model_output = model_output.strip()
    if start_index == -1 or model_output[0] != '(':
        return PipelineResult("SyntaxError", "NoPDDL", f"Could not find opening ( in ```{action_str}```")

    closing_index = matching_closing_paren(model_output)
    if closing_index is None:
        return PipelineResult("SyntaxError", "ParenMismatch", f"Could not find closing ) in ```{action_str}```")
    
    action_str : str = model_output[start_index:closing_index+1]
    if ":action" not in action_str:
        return PipelineResult("SyntaxError", "NoAction", f"Unable to find :action in ```{action_str}```")
    elif ":parameters" not in action_str:
        return PipelineResult("SyntaxError", "NoParams", f"Unable to find :parameters in ```{action_str}```")
    elif ":precondition" not in action_str:
        return PipelineResult("SyntaxError", "NoPrecond", f"Unable to find :precondition in ```{action_str}```")
    elif ":effect" not in action_str:
        return PipelineResult("SyntaxError", "NoEffect", f"Unable to find :effect in ```{action_str}```")

    return action_str

def pred_syntax_check(preds : list[str]) -> list[str] | PipelineResult:
    """
    Goes through each predicate in the model output and checks if it is valid
    """
    for pred in preds:
        start_index : int = pred.find("(")
        pred : str = pred[start_index:]

        if start_index == -1 or pred[0] != '(':
            return PipelineResult("SyntaxError", "NoPred", f"Could not find opening ( in ```{pred}```")
        
        pred = pred.strip()
        closing_index = matching_closing_paren(pred)
        if closing_index is None:
            return PipelineResult("SyntaxError", "NoPred", f"Could not find closing ) in ```{pred}```")

        pred_regex = r"\(\w+(\-\w+)?( \?\w+ - \w+)*\)"
        if not re.match(pred_regex, pred):
            return PipelineResult("SyntaxError", "NoPred", f"Invalid predicate syntax in ```{pred}``` ex (on ?x - block ?y - block)")
        
    return preds

def action_domain_template(domain_name: str, types : list[str], preds: list[str], action : str) -> str:
    """
    Given the components of the domain, types & preds & action, return a string of the domain
    """
    types_str = "\n".join(types)
    preds_str = "\n".join(preds)
    return f"""
        (define (domain test)
            (:requirements :strips :typing)
            (:types {types_str})
            (:predicates {preds_str})

            {action}
        )
    """

def check_output(p : Params, types : list[str], preds: list [str], action_str : str) -> None | PipelineResult:
    """
    Converts a pddl string to a PDDL action object or returns an error
    """
    # Check if the predicates are valid
    if (res := pred_syntax_check(preds)) is PipelineResult:
        return res

    # Check if the action string is valid
    if (res := action_syntax_check(action_str)) is PipelineResult:
        return res

    #return None
    action_domain = action_domain_template(p.domain_name, types, preds, action_str)
    try:
        _ = DOMAIN_PARSER(action_domain)
        return None
    except Exception as e:
        return PipelineResult("SyntaxError", "ParseError", f"Unable to parse action ```{action_str}```\nError: {repr(e)}")

# Initialize the LLMs
models = {
    provider : {model_name : init_chat_model(model_name, model_provider=provider) 
    for model_name in MODELS[provider]} 
    for provider in MODELS.keys()}


def llm_get_action(messages : List[BaseMessage], p : Params) -> Any | PipelineResult:
    """Calls the LLM and tries to parse the output as an action"""
    model = models[p.provider][p.model]
    response = model.invoke(messages)

    if response is None or response.content is None:
        logging.error(f"Model error: {response.error}")
        return PipelineResult("ModelError", "NoResponse", "Model returned no response")
    
    response_str = response.content
    messages.append(AIMessage(response_str))
    # Parse the response
    response_json = json.loads(response_str)
    if "types" not in response_json:
        return PipelineResult("SyntaxError", "NoTypes", f"Unable to find types in ```{response_str}```")
    if "predicates" not in response_json:
        return PipelineResult("SyntaxError", "NoPredicates", f"Unable to find predicates in ```{response_str}```")
    if "pddl_action" not in response_json:
        return PipelineResult("SyntaxError", "NoAction", f"Unable to find pddl_action in ```{response_str}```")

    types = response_json["types"]
    predicates = response_json["predicates"]
    action_str = response_json["pddl_action"]
    
    res = check_output(p, types, predicates, action_str)
    if res is not None:
        return res
    
    # Append the response to the message history to prepare for the next loop
    
    return response_json

def llm_get_action_retry(msgs : List[BaseMessage], p : Params, retry_limit : int) -> Any | PipelineResult:
    retries = 0
    res = None
    while retries < retry_limit:
        res = llm_get_action(msgs, p)
        if isinstance(res, PipelineResult):
            logging.error(f"Error: {res}")
            if res.error_type == "ModelError":
                raise RuntimeError(f"SHOULD NEVER HAPPEN, Model call failed!")
            else:
                msgs.append(HumanMessage(res.message + " \nPlease correct the error and try again."))
        else:
            return res
        retries += 1
    if retries == retry_limit:
        logging.error(f"Retry limit reached: {retry_limit}")
        return res
    raise RuntimeError(f"SHOULD NEVER HAPPEN, Model call failed!")
        

def domain_template(domain_name : str, outputs: list[Any]) -> str:
    """
    Given the components of the domain, types & preds & action, return a string of the domain
    """
    types = "\n".join(outputs[-1]["types"])
    preds = "\n".join(outputs[-1]["predicates"])
    actions = "\n".join(map(lambda x: x["pddl_action"], outputs))
    return f"""
        (define (domain {domain_name})
            (:requirements :strips :typing)
            (:types {types})
            (:predicates {preds})

            {actions}
        )
    """
    
    
