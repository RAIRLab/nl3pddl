'''
This script functions as the driver for the problem_generators module,
which creates generates randomized problems at various levels of difficulty for
the domains we evaluate over. 
'''

import os
import shutil
from typing import Any, Callable

from kstar_planner import planners

from nl3pddl.problem_generators import PROBLEM_GENERATORS
from nl3pddl.logger import logger
import nl3pddl.config as config
from pathlib import Path


def plan_file(
    domain_path : Path,
    problem_path : Path,
) -> dict | None:
    """
    Given a domain path and a problem invoke K* and produce k optimal plans as
    a json plans object.
    """
    
    # passing in domain_path as str gives error as kstar expects Path type
    plan_obj = planners.plan_topk(
        domain_file = domain_path,
        problem_file = problem_path,
        number_of_plans_bound = config.PLANS_PER_PROBLEM,
        timeout = config.KSTAR_TIMEOUT
    )
    if plan_obj.get("unsolvable", False):
        print("No plan found for domain and problem")
        return None
    return plan_obj

def plan_to_string(plan_obj : dict[str, Any]) -> str:
    """
    Return a VAL parsable plan from json object output by K*
    """
    plan_actions = plan_obj["actions"]
    result_plan_string : str = ""
    for action_str in plan_actions:
        result_plan_string += "(" + action_str + ")\n"
    return result_plan_string

def gen_problem_till_success(
        generator : Callable[[int, Path], None],
        i : int, 
        problem_file : Path, 
        domain_file : Path
) -> dict[str, Any]: 
    while True:
        generator(i, problem_file)
        print(f"Generated {problem_file}")
        plans = plan_file(
            domain_file, problem_file
        )
        if plans is None:
            logger.error(
                f"Failed to gen plans for {problem_file}, retrying..."
            )
            continue
        return plans["plans"]

def gen_domain_problems(domain_name, generator): 
    domain_file = f"data/domains/{domain_name}/ground.pddl"
    domain_file = Path(domain_file)
    assert os.path.exists(domain_file), \
        f"Domain file {domain_file} does not exist. " \
        "Please ensure the domain is generated first."
    
    problem_counts = {
        config.FEEDBACK_PROBLEMS_DIR: config.NUM_FEEDBACK_PROBLEMS,
        config.EVAL_PROBLEMS_DIR: config.NUM_EVAL_PROBLEMS
    }
    #Create problems director if it doesn't exist

    for dir_path, num_problems in problem_counts.items():
        output_dir = os.path.join(dir_path, domain_name)
        os.makedirs(output_dir, exist_ok=True)
        for i in range(1, num_problems + 1):
            problem_file = os.path.join(output_dir, f"problem-{i}.pddl")
            problem_file = Path(problem_file)
            # Try generating a problem and plans on it, fail if impossible
            # The number of plans is determined by config.KSTAR_N_PLANS
            plans = gen_problem_till_success(generator, i, problem_file, domain_file)
            # Write each plan to a file
            for j, plan in enumerate(plans):
                print(f"Generated plan for {problem_file}: {plan}")
                plan_str = plan_to_string(plan)
                plan_path = os.path.join(
                    output_dir, 
                    f"plan-{i}-{j}.txt"
                )
                with open(plan_path, 'w', encoding='utf-8') as file:
                    file.write(plan_str)

def generate_problems() -> None:
    if os.path.exists(config.GENERATED_PROBLEMS_DIR):
        shutil.rmtree(config.GENERATED_PROBLEMS_DIR)
    for domain, generator in PROBLEM_GENERATORS.items():
        if domain in config.DOMAINS:
            print(f"Generating problems for domain {domain}")
            gen_domain_problems(domain, generator)
