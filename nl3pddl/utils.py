"""
Utility functions for working with PDDL problems and domains.
"""

import json
import os
from typing import List, Tuple

from pddl.core import Problem
from pddl.core import Predicate

from .dataset import Dataset
from .logger import logger

CONFIG_FILE_PATH = "data/config.json"

def get_new_domains() -> list[str]:
    """
    Returns a list of paths of folders in data/domains
    marked as new in data/config.json
    """
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    new_domains = []
    for domain in config["new_domains"]:
        domain_path = os.path.join("data/domains", domain)
        if os.path.isdir(domain_path):
            new_domains.append(domain_path)
        else:
            logger.warning("Domain path %s is listed as a new \
            domain in data/config.json but does not exist.", domain_path)
    return new_domains

def parse_plan(plan_path: str) -> List[Tuple[str, List[str]]]:
    """Parses a plan file into a list of actions and their parameters."""
    with open(plan_path, "r", encoding="utf-8") as f:
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
    return [(pred.name, [arg.name for arg in pred.terms])
            for pred in problem.init]

def get_goal_preds(problem: Problem) -> List[Tuple[str, List[str]]]:
    """Returns a set of predicates in the goal state of the problem."""
    if hasattr(problem.goal, "operands"):
        return [(pred.name, [arg.name for arg in pred.terms])
                for pred in problem.goal.operands]
    else:
        return [(problem.goal.name, [arg.name for arg in problem.goal.terms])]

def get_all_preds(problem: Problem) -> List[Tuple[str, List[str]]]:
    """Returns a list of predicates in the initial
       state and goal of the problem."""
    init_preds = get_init_preds(problem)
    goal_preds = get_goal_preds(problem)
    return init_preds + goal_preds

def get_all_pred_names(problem: Problem) -> set[str]:
    """Returns a list of predicates in the initial state
       and goal of the problem."""
    return {pred[0] for pred in get_all_preds(problem)}

def get_all_pred_signatures(problem: Problem) -> set[str]:
    """Returns a list of predicates in the initial 
       state and goal of the problem."""
    return {pred[0] + "(" + ",".join(pred[1]) + ")" for pred in get_all_preds(problem)}

def get_all_pred_names_domain(d : Dataset, domain_path: str) -> set[str]:
    """For a given domain, get the list of all
       predicates in the initial state and goal of all problems."""
    all_pred_names = set()
    for problem_path in d.feedback_problem_paths[domain_path]:
        all_pred_names= all_pred_names.union(get_all_pred_names(d.feedback_problems[problem_path]))
    return all_pred_names

def get_all_pred_signatures_domain(d : Dataset, domain_path: str) -> set[str]:
    """
    For a given domain, get the list of all predicates in
    the initial state and goal of all problems.
    """
    all_pred_signatures = set()
    for problem_path in d.feedback_problem_paths[domain_path]:
        problem_preds = get_all_pred_signatures(d.feedback_problems[problem_path])
        all_pred_signatures = all_pred_signatures.union(problem_preds)
    return all_pred_signatures

def get_all_type_names(problem: Problem) -> set[str]:
    """Returns a list of types in the initial state and goal of the problem."""
    return {o.type_tag for o in problem.objects}

def get_all_type_names_domain(d : Dataset, domain_path: str) -> set[str]:
    """
    For a given domain, get the list of all types in 
    the initial state and goal of all problems.
    """
    all_type_names = set()
    for problem_path in d.feedback_problem_paths[domain_path]:
        problem_types = get_all_type_names(d.feedback_problems[problem_path])
        all_type_names = all_type_names.union(problem_types)
    return all_type_names

def pred_to_str(p : Predicate) -> str:
    """
    Converts a Predicate object to a string representation.
    Assumes only one type per argument.
    """
    name = p.name
    vars = [t.name for t in p.terms]
    types = [[tag for tag in t.type_tags][0] for t in p.terms]

    args = [f"?{var} - {type_}" for var, type_ in zip(vars, types)]
    return f"({name} {' '.join(args)})"

def grounded_pred_to_lm_str(p: Predicate) -> str:
    """Return landmark-style string for a grounded predicate or its negation.

    The landmark generator sometimes feeds us a Not(...) object
    from the problem init. If we naively try `p.name` on that, we blow up.
    Handle negation explicitly and return "NegatedAtom name(args)" to match
    how landmark facts are labeled elsewhere. Positive atoms stay as
    "Atom name(args)".
    """
    cls_name = p.__class__.__name__.lower()

    # If this is a Not node, unwrap it to its inner predicate.
    if cls_name == "not" or hasattr(p, "negated") or hasattr(p, "operand"):
        inner = getattr(p, "negated", None) or getattr(p, "operand", None)
        if inner is not None and hasattr(inner, "name") and hasattr(inner, "terms"):
            name = inner.name
            vars_ = [t.name for t in inner.terms]
            return f"NegatedAtom {name}({', '.join(vars_)})"

        s = str(p).strip()
        # Expected form: (not (pred arg1 arg2 ...))
        if s.startswith("(not "):
            inner_str = s[len("(not "):].strip()
            if inner_str.endswith(")"):
                inner_str = inner_str[:-1].strip()
            # inner_str should now look like: (pred arg1 arg2)
            if inner_str.startswith("(") and inner_str.endswith(")"):
                inner_core = inner_str[1:-1].strip()
            else:
                inner_core = inner_str
            parts = inner_core.split()
            if parts:
                name = parts[0]
                args = ", ".join(parts[1:])
                return f"NegatedAtom {name}({args})"
        return f"NegatedAtom {s}"

    # Positive atom path
    name = p.name
    vars_ = [t.name for t in p.terms]
    return f"Atom {name}({', '.join(vars_)})"
