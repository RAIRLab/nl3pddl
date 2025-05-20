"""
This file contains helpers for generating prompts for the LLM.

TODO: Parametrize out the prompts into their own files
"""


# LLM libs
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

# Internal imports
from nl3pddl.params import Params
from nl3pddl.dataset import Dataset
from nl3pddl.utils import get_all_type_names_domain, get_all_pred_signatures_domain

SYSTEM_PROMPT = SystemMessage("""
You will be given a natural language description of an a Planning Domain Definition Language (PDDL) domain along with a set of types and predicates 
you are allowed to use. You will then be given a description of each action and asked to use the provide PDDL, filling in the preconditions
and effects for each action. You are allowed to create new predicates as needed but must include the set of all predicates you used in the output.
For your output please provide a JSON object with the following felids: a string containing a raw PDDL action string, and a list of strings
containing the names of the predicates used in all actions so far. The JSON object should be formatted as follows:

{
    "pddl_action": "<raw PDDL action string>",
    "predicates": ["<predicate1>", "<predicate2>", ...]
    "types" : ["<type1>", "<type2>", ...]
}                          
""")

ACTION_PROMPT_TEMPLATE = PromptTemplate(template="""
Using the current list of predicates and any new predicates you feel you need, generate for the described action in the above described domain. 

{action_nl}

Regardless of whether you create any new predicates, include the set of all predicates used so far in the output.
""")

INIT_PROMPT_TEMPLATE = PromptTemplate(template="""
The following is a natural language description of a PDDL domain:

{domain_nl}

To start you may use the following types but are free to add more:

{types_nl}                                         

To start you may use the following predicates but are free to add more:

{predicates_nl}
""")

CONTEXT_EXAMPLES = [
HumanMessage("""
The following is a natural language description of a PDDL domain:

The domain assumes a world where there are a set of blocks that can
be stacked on top of each other, an arm that can hold one block at
a time, and a table where blocks can be placed.

To start you may use the following predicates but are free to add more:

["(handempty)", "(on ?x - block ?y - block)", "(ontable ?x - block)", "(clear ?x - block)", "(holding ?x - block)"]
"""),
HumanMessage("""
Using the current list of predicates and any new predicates you feel you need, generate a desc described action in the above described domain. 

The pick-up action represents the action of a robot arm picking up a single block from the table

Regardless of whether you create any new predicates, include the set of all predicates used so far in the output.
"""),
AIMessage("""
\{ 
    "pddl_action": "(:action pick-up \n\t:parameters (?x - block)\n\t:precondition (and (ontable ?x) (clear ?x) (handempty))\n\t:effect (and (not (ontable ?x)) (holding ?x) (not (handempty)) (not (clear ?x)))\n)",
    "predicates": ["(handempty)", "(on ?x - block ?y - block)", "(ontable ?x - block)", "(clear ?x - block)", "(holding ?x - block)"],
    "types": ["block"]
\}
"""),

HumanMessage("""
Using the current list of predicates and any new predicates you feel you need, generate a desc described action in the above described domain. 

The Stack action represents the action of stacking a block on top of another block. 

Regardless of whether you create any new predicates, include the set of all predicates used so far in the output.
"""),
AIMessage(""" 
{
    "pddl_action": "(:action stack \n\t:parameters (?x ?y - block)\n\t:precondition (and (clear ?y) (on ?x) (handempty))\n\t:effect (and (not (on ?x)) (not (handempty)) (stacked ?x ?y) (not (clear ?y)))\n)",
    "predicates": ["handempty", "on", "ontable", "clear", "stacked", "block"]
    "types": ["block"]
} 
""")
]


def init_msgs(d: Dataset, p : Params) -> list[BaseMessage]:
    """
    Generates the initial messages list for the LLM to start with
    """

     # Start off constructing a chat completion message history with the system prompt and context     
    messages = [SYSTEM_PROMPT, *CONTEXT_EXAMPLES]

    # Get the predicates and types from the domain
    types_nl = "[" + ", ".join(get_all_type_names_domain(d, p.domain_path)) + "]"

    predicates_nl = None
    # Change the initial prompt based off of whether we want to include pred descriptions or not
    if p.give_pred_descriptions:
        description_pairs = []
        for pred_sig in get_all_pred_signatures_domain(d, p.domain_path):
            pred_name = pred_sig.split("(")[0]
            description_pairs.append((pred_name, d.nl_json[p.domain_path]["predicates"][pred_name][p.desc_class]))
        predicates_nl = "[" + ", ".join([f"{pred_name}: {pred_desc}" for pred_name, pred_desc in description_pairs]) + "]"
    else:
        predicates_nl = "[" + ", ".join(get_all_pred_signatures_domain(p.domain_path)) + "]"

    messages.append(HumanMessage(INIT_PROMPT_TEMPLATE.format(
        domain_nl=d.nl_json[p.domain_path]["overall"][p.desc_class],
        predicates_nl=predicates_nl,
        types_nl=types_nl
    )))

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