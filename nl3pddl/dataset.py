""" Dataset class and loader for the NL3PDDL project. """

import json
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

from tqdm import tqdm
import pddl
from pddl.core import Domain, Problem

from .logger import logger

#TODO: this should be moved to a config file, we redefine it in gen_problems.py
PLANS_PER_PROBLEM = 2
TEMPLATE_FILE_NAME = "template.pddl.txt"
GROUND_TRUTH_FILE_NAME = "ground.pddl"
NL_FILE_NAME = "nl.json"
FEEDBACK_PROBLEM_DIR = "data/gen_problems/feedback"
EVALUATION_PROBLEM_DIR = "data/gen_problems/evaluation"
LANDMARK_PROBLEM_DIR = "data/gen_landmarks" #Landmarks are only for testing problems

def domains() -> list[str]:
    """returns a list of paths of folders in data/domains"""
    domain_paths = []
    for root, dirs, files in os.walk("data/domains"):
        for dir_name in dirs:
            domain_path = os.path.join(root, dir_name)
            if os.path.isdir(domain_path):
                domain_paths.append(dir_name)
    return domain_paths

def get_new_domains() -> list[str]:
    """returns a list of paths of folders in data/domains
       marked as new in data/config.json"""
    new_domains = []
    for domain in domains():
        domain_path = os.path.join("data/domains", domain)
        if os.path.isdir(domain_path):
            new_domains.append(domain_path)
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

@dataclass
class PipelineResult:
    """ 
    This class models an error in the output of the model, 
    with two levels of error class and a message indicating exactly
    what went wrong such that it can be passed back to the model and
    used for fixing the error
    """
    # For classification purposes
    major_class : str
    # For classification purposes
    minor_class : str
    # Natural language description of the error,
    # may be passed back to the model for looping
    message : str

class Dataset:
    """
    The Dataset contains paths, raws, and parsed asts for each 
    domain, problem, and plan, along with the relations between them.
    """
    # Relative paths to domain folders
    domain_paths : List[str] = []

    # Dictionary from domain folders to an AST Domain object
    # representing the Ground truth domain in the folder
    domains : Dict[str, Domain] = {}

    # Dictionary from domain paths to a list of paths
    # to problem files in the folder
    feedback_problem_paths : Dict[str, List[str]] = {}

    # Dictionary from problem paths to problem strings
    feedback_problem_raws: Dict[str, str] = {}

    # Dictionary from problem paths to an AST Problem object
    feedback_problems : Dict[str, Problem] = {}

    # Dictionary from problem paths to for now a single plan paths.
    feedback_plan_paths : Dict[str, list[str]] = {}

    feedback_plan_raws : Dict[str, str] = {}

    # Dictionary from plan paths to a wrong problem path,
    wplan_paths : Dict[str, str] = {}

    # "AST" of the plan, maps a single plan path to its "AST", a list of
    # actions and their arguments.
    feedback_plans : Dict[str, List[Tuple[str, List[str]]]] = {}

    evaluation_problem_paths : Dict[str, List[str]] = {}
    evaluation_problem_raws : Dict[str, str] = {}
    evaluation_plan_paths : Dict[str, List[str]] = {}
    evaluation_plan_raws : Dict[str, str] = {}

    # Dictionary from plan paths to their raw string representation
    plan_raws : Dict[str, str] = {}

    wplan_raws : Dict[str, str] = {}

    # NL descriptions of the predicates and actions in the domain
    nl_json : Dict[str, Any] = {}

    # Landmark actions, maps a problem path to a landmark which is a list of lists of disjunctive actions that must be satisfied for the problem to be solved.
    landmarks: Dict[str, List[List[str]]] = {}

    def __init__(self):
        """ 
        Reads the dataset from the data/domains folder and parses it into
        the internal data structures of the Dataset class.
        """
        self.domain_paths = get_new_domains()
        for domain_path in tqdm(self.domain_paths, "Parsing Domains"):
            ground_path = os.path.join(domain_path, GROUND_TRUTH_FILE_NAME)
            try:
                domain = pddl.parse_domain(ground_path)
            except Exception as e:
                logger.error("Error parsing domain %s: %s", ground_path, e)
                exit(1)

            self.domains[domain_path] = domain

            # Read the feedback problems
            feedback_dir : str = os.path.join(FEEDBACK_PROBLEM_DIR, domain.name)
            landmark_dir : str = os.path.join(LANDMARK_PROBLEM_DIR, domain.name)
            feedback_problem_paths = \
                [os.path.join(feedback_dir, f) for f in
                 os.listdir(feedback_dir) if f.endswith(".pddl")]
            self.feedback_problem_paths[domain_path] = feedback_problem_paths

            for problem_path in feedback_problem_paths:
                # extract i from the name of the problem file, e.g. problem-1.pddl -> 1
                i = int(os.path.basename(problem_path).split("-")[1].split(".")[0])
                with open(problem_path, "r", encoding="utf-8") as f:
                    self.feedback_problem_raws[problem_path] = f.read()
                try:
                    problem = pddl.parse_problem(problem_path)
                except Exception as e:
                    logger.error("Error parsing problem file %s: %s",
                                   problem_path, e)
                    exit(1)
                
                self.feedback_problems[problem_path] = problem
                self.feedback_plan_paths[problem_path] = \
                    [os.path.join(feedback_dir, f"plan-{i}-{j}.txt") for j in
                     range(1, PLANS_PER_PROBLEM + 1)]
                for plan_path in self.feedback_plan_paths[problem_path]:
                    if os.path.exists(plan_path):
                        self.feedback_plans[plan_path] = parse_plan(plan_path)
                        with open(plan_path, "r", encoding="utf-8") as f:
                            self.feedback_plan_raws[plan_path] = f.read()
                
                problem_name = os.path.basename(problem_path)
                problem_name = problem_name.replace(".pddl", ".json")
                landmark_path = os.path.join(landmark_dir, problem_name)
                with open(landmark_path, "r", encoding="utf-8") as f:
                    self.landmarks[problem_path] = json.load(f)["landmarks"]

            # Read the evaluation problems
            problem_dir = os.path.join(EVALUATION_PROBLEM_DIR, domain.name)
            self.evaluation_problem_paths[domain_path] = \
                [os.path.join(problem_dir, f) for f in os.listdir(problem_dir) \
                 if f.endswith(".pddl")]
            for problem_file in self.evaluation_problem_paths[domain_path]:
                i = int(os.path.basename(problem_file).split("-")[1].split(".")[0])
                with open(problem_file, "r", encoding="utf-8") as f:
                    self.evaluation_problem_raws[problem_file] = f.read()
                self.evaluation_plan_paths[problem_file] = [os.path.join(problem_dir, f"plan-{i}-{j}.txt") for j in range(1, PLANS_PER_PROBLEM + 1)]
                for plan_path in self.evaluation_plan_paths[problem_file]:
                    if os.path.exists(plan_path):
                        with open(plan_path, "r", encoding="utf-8") as f:
                            self.evaluation_plan_raws[plan_path] = f.read()

            nl_file_path = os.path.join(domain_path, NL_FILE_NAME)
            with open(nl_file_path, "r", encoding="utf-8") as f:
                self.nl_json[domain_path] = json.load(f)
