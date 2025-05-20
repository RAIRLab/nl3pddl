

import json
import logging
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

from tqdm import tqdm

import pddl
from pddl.core import Domain, Problem
from pddl.formatter import domain_to_string

CONFIG_FILE_PATH = "data/config.json"
CONFIG_FILE_PATH = "data/config.json"
TEMPLATE_FILE_NAME = "template.pddl.txt"
GROUND_TRUTH_FILE_NAME = "ground.pddl"
NL_FILE_NAME = "nl.json"

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

@dataclass
class PipelineResult:
    """ 
    This class models an error in the output of the model, 
    with two levels of error class and a message indicating exactly what went wrong
    such that it can be passed back to the model and used for fixing the error
    """
    # For classification purposes
    major_class : str
    # For classification purposes
    minor_class : str
    # Natural language description of the error, may be passed back to the model for looping
    message : str

class Dataset:
    """Experiment context"""
    # Relative paths to domain folders    
    domain_paths : List[str] = []

    # Dictionary from domain folders to an AST Domain object representing the 
    # Ground truth domain in the folder
    domains : Dict[str, Domain] = {}

    # Dictionary from domain paths to a list of paths to problem files in the folder
    problem_paths : Dict[str, List[str]] = {}

    # Dictionary from problem paths to problem strings
    problem_raws: Dict[str, str] = {}

    # Dictionary from problem paths to an AST Problem object
    problems : Dict[str, Problem] = {}

    # Dictionary from problem paths to for now a single plan paths.
    plan_paths : Dict[str, str] = {}

    # "AST" of the plan, maps a single plan path to its "AST", a list of actions and their arguments.
    plans : Dict[str, List[Tuple[str, List[str]]]] = {}

    # Dictionary from plan paths to their raw string representation
    plan_raws : Dict[str, str] = {}

    # NL descriptions of the predicates and actions in the domain
    nl_json : Dict[str, Any] = {}

    def __init__(self):
        self.domain_paths = get_new_domains()
        for domain_path in tqdm(self.domain_paths, "Parsing Domains"): 
            domain = pddl.parse_domain(os.path.join(domain_path, GROUND_TRUTH_FILE_NAME))
            self.domains[domain_path] = domain
            self.problem_paths[domain_path] = \
                [os.path.join(domain_path, f) for f in os.listdir(domain_path) if f.startswith("p") and f.endswith(".pddl")]
            for problem_file in self.problem_paths[domain_path]:
                with open(problem_file, "r") as f:
                    self.problem_raws[problem_file] = f.read()
                problem = pddl.parse_problem(problem_file)
                self.problems[problem_file] = problem
                plan_path = problem_file.replace(".pddl", ".plan.txt")
                self.plan_paths[problem_file] = plan_path
                with open(plan_path, "r") as f:
                    self.plan_raws[plan_path] = f.read()
                self.plans[plan_path] = parse_plan(self.plan_paths[problem_file])
            with open(os.path.join(domain_path, NL_FILE_NAME), "r") as f:
                self.nl_json[domain_path] = json.load(f)