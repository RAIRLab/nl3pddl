
# Standard Libs
import json
import logging
import copy
import itertools
import os
from typing import List, Tuple, Dict, Any

# PDDL Parsing
import pddl
from pddl.core import Domain, Problem, Action
from pddl.parser.domain import DomainParser
from pddl.formatter import domain_to_string

# LLM libs
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate

load_dotenv()

ACTION_PROMPT_TEMPLATE = "prompts/action.txt"
SYSTEM_PROMPT_TEMPLATE = "prompts/system.txt"
INIT_PROMPT_TEMPLATE = "prompts/init.txt"
REPROMPT_PROMPT_TEMPLATE = "prompts/reprompt.txt"

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")

DB_FILE_PATH = "data/domains.db"
CONFIG_FILE_PATH = "data/config.json"
TEMPLATE_FILE_NAME = "template.pddl.txt"
GROUND_TRUTH_FILE_NAME = "ground.pddl"
NL_FILE_NAME = "nl.json"

# Number of reprompt attempts to make before giving up
REPROMPT_THRESHOLD = 5

# Provider model dictionary
MODEL_IDS = {
    "gpt-4o-mini", "gpt-4", "o4-mini"
}

# Give predicate descriptions to prompts?
GIVE_PRED_DESCRIPTIONS = True

# Utility functions ===========================================================

def get_new_domains() -> list[str]:
    """returns a list of paths of folders in data/domains marked as new in data/config.json"""
    with open(CONFIG_FILE_PATH, "r") as f:
        config = json.load(f)
    new_domains = []
    for domain in config["new_domains"]:
        domain_path = os.path.join("data/domains", domain)
        if os.path.isdir(domain_path):
            new_domains.append(domain_path)
        else:
            logging.warning(f"Domain path {domain_path} is listed as a new domain in data/config.json but does not exist.")
    return new_domains

def parse_plan(plan_path: str) -> List[Tuple[str, List[str]]]:
    """Parses a plan file into a list of actions and their parameters."""
    with open(plan_path, "r") as f:
        lines = f.readlines()
    plan = []
    for line in lines:
        line = line.strip()
        if line.startswith("(") and line.endswith(")"):
            action = line[1:-1].split()
            action_name = action[0]
            parameters = action[1:]
            plan.append((action_name, parameters))
    return plan

def get_init_preds(problem: Problem) -> List[Tuple[str, List[str]]]:
    """Returns a set of predicates in the initial state of the problem."""
    return [(pred.name, [arg.name for arg in pred.terms]) for pred in problem.init]

def get_goal_preds(problem: Problem) -> List[Tuple[str, List[str]]]:
    """Returns a set of predicates in the goal state of the problem."""
    return [(pred.name, [arg.name for arg in pred.terms]) for pred in problem.init]

def get_all_preds(problem: Problem) -> List[Tuple[str, List[str]]]:
    """Returns a list of predicates in the initial state and goal of the problem."""
    init_preds = get_init_preds(problem)
    goal_preds = get_goal_preds(problem)
    return init_preds + goal_preds

def get_all_pred_names(problem: Problem) -> set[str]:
    """Returns a list of predicates in the initial state and goal of the problem."""
    return {pred[0] for pred in get_all_preds(problem)}

def get_all_pred_signatures(problem: Problem) -> set[str]:
    """Returns a list of predicates in the initial state and goal of the problem."""
    return {pred[0] + "(" + ",".join(pred[1]) + ")" for pred in get_all_preds(problem)}

def get_all_pred_names_domain(domain_path: str) -> set[str]:
    """For a given domain, get the list of all predicates in the initial state and goal of all problems."""
    all_pred_names = set()
    for problem_path in problem_paths[domain_path]:
        all_pred_names= all_pred_names.union(get_all_pred_names(problems[problem_path]))
    return all_pred_names

def get_all_pred_signatures_domain(domain_path: str) -> set[str]:
    """For a given domain, get the list of all predicates in the initial state and goal of all problems."""
    all_pred_signatures = set()
    for problem_path in problem_paths[domain_path]:
        all_pred_signatures = all_pred_signatures.union(get_all_pred_signatures(problems[problem_path]))
    return all_pred_signatures

def get_all_type_names(problem: Problem) -> set[str]:
    """Returns a list of types in the initial state and goal of the problem."""
    return {o.type_tag for o in problem.objects}

def get_all_type_names_domain(domain_path: str) -> set[str]:
    """For a given domain, get the list of all types in the initial state and goal of all problems."""
    all_type_names = set()
    for problem_path in problem_paths[domain_path]:
        all_type_names = all_type_names.union(get_all_type_names(problems[problem_path]))
    return all_type_names

# Pipeline Start ============================================================

models = {model_name: init_chat_model(model_name, model_provider="openai") for model_name in MODEL_IDS}

# Relative paths to domain folders    
domain_paths = get_new_domains()

# Dictionary from domain folders to an AST Domain object representing the 
# Ground truth domain in the folder
domains : Dict[str, Domain] = {}

# Dictionary from domain paths to a list of paths to problem files in the folder
problem_paths : Dict[str, List[str]] = {}

# Dictionary from problem paths to an AST Problem object
problems : Dict[str, Problem] = {}

# Dictionary from problem paths to for now a single plan paths.
plan_paths : Dict[str, str] = {}

# "AST" of the plan, maps a single plan path to its "AST", a list of actions and their arguments.
plans : Dict[str, List[Tuple[str, List[str]]]] = {}

# NL descriptions of the predicates and actions in the domain
nl_json : Dict[str, Any] = {}

#Array of every file with the name p*.pddl in the domain folder, use regex to get the name of the problem
for domain_path in domain_paths: 
    domain = pddl.parse_domain(os.path.join(domain_path, GROUND_TRUTH_FILE_NAME))
    domains[domain_path] = domain
    problem_paths[domain_path] = [os.path.join(domain_path, f) for f in os.listdir(domain_path) if f.startswith("p") and f.endswith(".pddl")]
    for problem_file in problem_paths[domain_path]:
        problem = pddl.parse_problem(problem_file)
        problems[problem_file] = problem
        plan_paths[problem_file] = problem_file.replace(".pddl", ".plan.txt")
        plans[problem_file] = parse_plan(plan_paths[problem_file])
    with open(os.path.join(domain_path, NL_FILE_NAME), "r") as f:
        nl_json[domain_path] = json.load(f)

print(domain_paths)
print(problem_paths)
print(plan_paths)

# Pipeline helpers ================================================================

# Taken from original NL2PDDL

def template_domain(domain : Domain):
    """ Creates a templated domain string for a single action in a domain """
    domain_copy = copy.deepcopy(domain)
    domain_copy._actions = {}  # nopep8
    domain_copy_str = domain_to_string(domain_copy)
    return domain_copy_str[:-2] + "{action})"

DOMAIN_TEMPLATES = {domain_name : template_domain(domain_obj) for domain_name, domain_obj in domains.items()}
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

def syntax_check(model_output : str) -> tuple[str, str, str, str]:
    """
    Returns None if the model outputs invalid PDDL, otherwise returns
    the string of the correct PDDL extracted from the model output
    """
    start_index : int = model_output.find("(")
    model_output : str = model_output[start_index:]
    model_output = model_output.strip()
    result : tuple[str, str, str, str]
    if start_index == -1 or model_output[0] != '(':
        result = None, "SyntaxError", "NoPDDL", "Could not find opening ("
    else:
        closing_index = matching_closing_paren(model_output)
        if closing_index is None:
            result = None, "SyntaxError", "ParenMismatch", "Could not find closing )"
        else:
            action_str : str = model_output[:closing_index+1]
            if ":action" not in action_str:
                result = None, "SyntaxError", "NoAction", "Unable to find :action"
            elif ":parameters" not in action_str:
                result = None, "SyntaxError", "NoParams", "Unable to find :parameters"
            elif ":precondition" not in action_str:
                result = None, "SyntaxError", "NoPrecond", "Unable to find :precondition"
            elif ":effect" not in action_str:
                result = None, "SyntaxError", "NoEffect", "Unable to find :effect"
            else:
                result = action_str, "", "", ""
    return result

def str_to_action(model_action_output : str, domain_name : str) \
-> tuple[Action, str, str, str]:
    """
    Converts a string to a PDDL action object. 
    """
    action_str, result_class, result_subclass, err_msg = \
        syntax_check(model_action_output)
    if action_str is None:
        return action_str, result_class, result_subclass, err_msg
    action_domain = DOMAIN_TEMPLATES[domain_name].format(action=action_str)
    try:
        tree = DOMAIN_PARSER(action_domain)
        for action in tree.actions:
            return action, "", "", ""
    except Exception as e:
        return None, "SyntaxError", "ParseError", repr(e)
    
def str_to_action_basic(model_action_output : str, domain_name : str) -> Action | None:
    """
    Attempts to convert a model output string to a PDDL action object.
    If it fails, return None.
    """
    str_to_action(model_action_output, domain_name)[0]

# Prompt generation ===========================================================

system_prompt = SystemMessage("""
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

action_prompt_template = PromptTemplate(template="""
Using the current list of predicates and any new predicates you feel you need, generate for the described action in the above described domain. 

{action_nl}

Regardless of whether you create any new predicates, include the set of all predicates used so far in the output.
""")

initial_prompt_template = PromptTemplate(template="""
The following is a natural language description of a PDDL domain:

{domain_nl}

To start you may use the following types but are free to add more:

{types_nl}                                         

To start you may use the following predicates but are free to add more:

{predicates_nl}
""")

context = [
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



# Main loop ================================================================

DESCRIPTION_CLASS = "detailed-first" # or "first"

results_map = {}

for (model_name, model), domain_path in itertools.product(models.items(), domain_paths):

    # Start off constructing a chat completion message history with the system prompt and context     
    messages = [system_prompt, *context]

    # Get the predicates and types from the domain
    types_nl = "[" + ", ".join(get_all_type_names_domain(domain_path)) + "]"

    predicates_nl = None
    if GIVE_PRED_DESCRIPTIONS:
        description_pairs = []
        for pred_sig in get_all_pred_signatures_domain(domain_path):
            pred_name = pred_sig.split("(")[0]
            description_pairs.append((pred_name, nl_json[domain_path]["predicates"][pred_name][DESCRIPTION_CLASS]))
        predicates_nl = "[" + ", ".join([f"{pred_name}: {pred_desc}" for pred_name, pred_desc in description_pairs]) + "]"
    else:
        predicates_nl = "[" + ", ".join(get_all_pred_signatures_domain(domain_path)) + "]"
    
    # Add the initial prompt to the message history
    messages.append(HumanMessage(initial_prompt_template.format(
        domain_nl=nl_json[domain_path]["overall"][DESCRIPTION_CLASS],
        predicates_nl=predicates_nl,
        types_nl=types_nl
    )))

    # TODO: add a retry decorator to the model call

    action_gen_failure_flag = False
    # Query the model for each action in the domain, building up the message history
    for action_name, action_descs in nl_json[domain_path]["actions"].items():
        action_nl = action_descs[DESCRIPTION_CLASS]
        
        messages.append(HumanMessage(action_prompt_template.format(
            action_nl=action_nl
        )))

        # Get the model response
        response = model.invoke(messages)
        response_str = response.content
        if response is None or response.content is None:
            logging.error(f"Model error: {response.error}")
            action_gen_failure_flag = True
            break
        print(f"Model response: {response_str}")

        # Parse the response
        response_json = json.loads(response_str)
        pddl_action = response_json["pddl_action"]
        action_ast = str_to_action(pddl_action, domain_path)

        # Append the response to the message history to prepare for the next loop
        messages.append(AIMessage(response_str))

    if action_gen_failure_flag:
        results_map[(model_name, domain_path)] = "Syntax"
        logging.error(f"Action generation failed for model {model_name} on domain {domain_path}")
        continue







        
        


