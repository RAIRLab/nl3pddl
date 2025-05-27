"""
This file contains helpers for generating prompts for the LLM.
"""

import os

# External package imports
from typing import Any
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    BaseMessage
)
from langchain_core.prompts import PromptTemplate

# Internal imports
from nl3pddl.params import Params
from nl3pddl.dataset import Dataset
from nl3pddl.utils import (
    get_all_type_names_domain,
    get_all_pred_signatures_domain
)

PROMPT_DIR = "data/prompts"

def load_prompt(prompt_file: str) -> str:
    """
    Loads a prompt from a file and returns it as a string.
    """
    prompt_path = os.path.join(PROMPT_DIR, prompt_file)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


SYSTEM_PROMPT = SystemMessage(load_prompt("1-system.txt"))

CONTEXT_EXAMPLES = [
    HumanMessage(load_prompt("2-context-domain.txt")),
    HumanMessage(load_prompt("3-context-action1-nl.txt")),
    AIMessage(load_prompt("4-context-action1-response.txt")),
    HumanMessage(load_prompt("5-context-action2-nl.txt")),
    AIMessage(load_prompt("6-context-action2-response.txt"))
]

INIT_PROMPT_TEMPLATE = PromptTemplate(template=load_prompt("7-domain.txt"))

ACTION_PROMPT_TEMPLATE = PromptTemplate(template=load_prompt("8-action.txt"))


def init_msgs(d: Dataset, p : Params) -> list[BaseMessage]:
    """
    Generates the initial messages list for the LLM to start with
    """

     # Start off constructing a chat completion message history with
     # the system prompt and context
    messages = [SYSTEM_PROMPT, *CONTEXT_EXAMPLES]

    # Get types and predicates for the domain
    types_list = ", ".join(get_all_type_names_domain(d, p.domain_path))
    types_list = "[" + types_list + "]"

    predicates_nl = None
    # Change the initial prompt based off of whether we
    # want to include pred descriptions or not
    if p.give_pred_descriptions:
        description_pairs = []
        pred_sigs = get_all_pred_signatures_domain(d, p.domain_path)
        names = {pred_sig.split("(")[0] for pred_sig in pred_sigs}
        for pred_name in names:
            description_pairs.append((
                pred_name,
                d.nl_json[p.domain_path]["predicates"][pred_name][p.desc_class])
            )
        predicates_nl = ", ".join([f"{pred_name}: {pred_desc}"
                              for pred_name, pred_desc in description_pairs])
        predicates_nl = "[" + predicates_nl + "]"
    else:
        pred_sigs = get_all_pred_signatures_domain(d, p.domain_path)
        predicates_nl = ", ".join(pred_sigs)
        predicates_nl = "[" + predicates_nl + "]"

    messages.append(HumanMessage(INIT_PROMPT_TEMPLATE.format(
        domain_nl=d.nl_json[p.domain_path]["overall"][p.desc_class],
        predicates_nl=predicates_nl,
        types_nl=types_list
    )))
    return messages

def action_message(d : Dataset, h : Params, action_name : str) -> HumanMessage:
    """
    Generates an action message given the domain and name
    """
    action_desc = d.nl_json[h.domain_path]["actions"][action_name][h.desc_class]

    return HumanMessage(ACTION_PROMPT_TEMPLATE.format(
        action_nl=action_desc
    ))

Part2 = HumanMessage("""
You have completed the following domain:                       
""")

def domain_template(domain_name : str, outputs: list[Any]) -> str:
    """
    Given the components of the domain, types & preds & action,
    return a string of the domain
    """
    types = "\n".join(outputs[-1].types)
    preds = "\n".join(outputs[-1].predicates)
    actions = "\n".join(map(lambda x: x.pddl_action, outputs))
    return f"""
        (define (domain {domain_name})
            (:requirements :strips :typing)
            (:types {types})
            (:predicates {preds})

            {actions}
        )
    """