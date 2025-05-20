

import re
from typing import Any

from pddl.core import Domain, Action
from pddl.parser.domain import DomainParser
from pddl.formatter import domain_to_string

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from .params import MODELS, Params
from .dataset import Dataset, PipelineResult



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

def check_action_output(p : Params, message : Any) -> None | str:
    """
    Converts a pddl string to a PDDL action object or returns an error
    """
    preds = message["predicates"]
    types = message["types"]
    action_str = message["pddl_action"]
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
        return HumanMessage(f"Unable to parse action ```{action_str}```\nError: {repr(e)} \nPlease revise the action and try again.")

def check_domain_output(p : Params, message : Any) -> None | str:
    """
    Converts a pddl string to a PDDL domain object or returns an error
    """
    domain_str = message["pddl_domain"]
    try:
        _ = DOMAIN_PARSER(domain_str)
        return None
    except Exception as e:
        return HumanMessage(f"Unable to parse domain ```{domain_str}```\nError: {repr(e)} \nPlease revise the domain and try again.")