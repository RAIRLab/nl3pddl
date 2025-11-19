"""
This file contains functions for checking the output of the LLM for
action and domain syntax and semantic feedback.
"""

# Standard library imports
import re
from typing import Any

# External package imports
from pddl.core import Domain
from pddl.parser.domain import DomainParser
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from nl3pddl.params import Params

# Internal package imports
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
        return PipelineResult("SyntaxError", "NoPDDL",
        f"Could not find opening ( in ```{model_output}``` this should be a \
        valid PDDL action of the form, (:action <action_name> \
        :parameters (<param1> - <type1> <param2> - <type2>) \
        :precondition (<pred1> <pred2>) :effect (<pred1> <pred2>) )")

    closing_index = matching_closing_paren(model_output)
    if closing_index is None:
        return PipelineResult("SyntaxError", "ParenMismatch",
            f"Could not find closing ) in ```{model_output}```")

    action_str : str = model_output[start_index:closing_index+1]
    if ":action" not in action_str:
        return PipelineResult("SyntaxError", "NoAction",
            f"Unable to find :action in ```{action_str}```")
    elif ":parameters" not in action_str:
        return PipelineResult("SyntaxError", "NoParams",
            f"Unable to find :parameters in ```{action_str}```")
    elif ":precondition" not in action_str:
        return PipelineResult("SyntaxError", "NoPrecond",
            f"Unable to find :precondition in ```{action_str}```")
    elif ":effect" not in action_str:
        return PipelineResult("SyntaxError", "NoEffect",
            f"Unable to find :effect in ```{action_str}```")

    return action_str

def pred_syntax_check(preds : list[str]) -> list[str] | PipelineResult:
    """
    Goes through each predicate in the model output and checks if it is valid
    """
    for pred in preds:
        start_index : int = pred.find("(")
        pred : str = pred[start_index:]

        if start_index == -1 or pred[0] != '(':
            return PipelineResult("SyntaxError", "NoPred",
                f"Could not find opening ( in ```{pred}```")

        pred = pred.strip()
        closing_index = matching_closing_paren(pred)
        if closing_index is None:
            return PipelineResult("SyntaxError", "NoPred",
                f"Could not find closing ) in ```{pred}```")

        pred_regex = r"\(\w+(\-\w+)?( \?\w+ - \w+)*\)"
        if not re.match(pred_regex, pred):
            return PipelineResult("SyntaxError", "NoPred",
                f"Invalid predicate syntax in ```{pred}```\
                ex (on ?x - block ?y - block)")
    return preds

def action_domain_template(
    types : list[str],
    preds: list[str],
    action : str
) -> str:
    """
    Given the components of the domain, types & preds & action,
    return a string of the domain
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

def lark_err_str(e : Exception) -> str:
    """
    Converts a lark parsing error to a human-readable string.
    """
    try:
        return f"Failed at position {e.pos_in_stream}\
                 with error: {e.token} as {e}"
    except Exception: # pylint: disable=broad-except
        #This should NEVER happen, come up with better cases.
        #Occasionally the lark error fails, this is the worst case
        #fallback scenario
        return "A parsing error occurred without an error message "

bad_pred_list_template = PromptTemplate(template="""
    The following predicate list you provided is invalid:
    {predicates}
    The error is: {error}
    Please note that the predicate list must be a types PDDL list of predicates in the form
    ["(predicate1 ?x - type1 ?y - type2 ...)", "(predicate2 ?x - type1 ?y - type2 ...), ...]
    where the types are defined in the domain.
    """)

def check_action_output(
    message : Any
) -> None | HumanMessage:
    """
    Converts a pddl string to a PDDL action object or returns an error
    """
    preds = message["predicates"]
    types = message["types"]
    action_str = message["pddl_action"]
    # Check if the predicates are valid
    res = pred_syntax_check(preds)
    if isinstance(res, PipelineResult):
        return HumanMessage(bad_pred_list_template.format(
            predicates=preds, 
            error=res.message
        ))

    # Check if the action string is valid
    res = action_syntax_check(action_str)
    if isinstance(res, PipelineResult):
        return HumanMessage(res.message)

    #return None if the action is valid, else error message
    action_domain = action_domain_template(types, preds, action_str)
    try:
        _ = DOMAIN_PARSER(action_domain)
        return None
    except Exception as e: # pylint: disable=broad-except
        return HumanMessage(f"Unable to parse action ```{action_str}```\n\
        Error: {lark_err_str(e)} \nPlease revise the action and try again. Remember that this must be a STRIPS action, it may not contain any additional PDDL features. I.E. there should be no 'or', 'forall', 'exists', or '=' anywhere in the action, and it may not contain negative preconditions.")

def check_domain_syntax_output(d : Dataset,p: Params, message : Any) -> None | HumanMessage:
    """
    Converts a pddl string to a PDDL domain object or returns an error
    """
    ground_domain : Domain = d.domains[p.domain_path]
    domain_str : str = message["pddl_domain"]
    try:
        domain : Domain = DOMAIN_PARSER(domain_str)
        if domain.name != ground_domain.name:
            return HumanMessage(f"Domain name {domain.name} does not match \
            expected domain name {ground_domain.name}. Please revise the domain \
            and try again.")
        # Check to make sure all action names match the ground domain
        ground_action_names = {a.name for a in ground_domain.actions}
        action_names = {a.name for a in domain.actions}
        if ground_action_names != action_names:
            missing = ground_action_names - action_names
            extra = action_names - ground_action_names
            msg = ""
            if missing:
                msg += f"Missing actions: {', '.join(missing)}. "
            if extra:
                msg += f"Extra actions: {', '.join(extra)}. "
            return HumanMessage(f"Action names do not match the expected action names. \n {msg} \n These are the only allowed action names: {', '.join(ground_action_names)}.\n Please revise the domain and try again.")
        return None
    except Exception as e: # pylint: disable=broad-except 
        return HumanMessage(f"Unable to parse domain ```{domain_str}```\nError: {lark_err_str(e)} \nRecall that this must be a STRIPS domain, it may not contain any additional PDDL features.")
