
import json
import logging
import os
from typing import List, Tuple


from pddl.core import Problem

from nl3pddl.dataset import Dataset

CONFIG_FILE_PATH = "data/config.json"

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

def get_all_pred_names_domain(d : Dataset, domain_path: str) -> set[str]:
    """For a given domain, get the list of all predicates in the initial state and goal of all problems."""
    all_pred_names = set()
    for problem_path in d.problem_paths[domain_path]:
        all_pred_names= all_pred_names.union(get_all_pred_names(d.problems[problem_path]))
    return all_pred_names

def get_all_pred_signatures_domain(d : Dataset, domain_path: str) -> set[str]:
    """For a given domain, get the list of all predicates in the initial state and goal of all problems."""
    all_pred_signatures = set()
    for problem_path in d.problem_paths[domain_path]:
        all_pred_signatures = all_pred_signatures.union(get_all_pred_signatures(d.problems[problem_path]))
    return all_pred_signatures

def get_all_type_names(problem: Problem) -> set[str]:
    """Returns a list of types in the initial state and goal of the problem."""
    return {o.type_tag for o in problem.objects}

def get_all_type_names_domain(d : Dataset, domain_path: str) -> set[str]:
    """For a given domain, get the list of all types in the initial state and goal of all problems."""
    all_type_names = set()
    for problem_path in d.problem_paths[domain_path]:
        all_type_names = all_type_names.union(get_all_type_names(d.problems[problem_path]))
    return all_type_names
