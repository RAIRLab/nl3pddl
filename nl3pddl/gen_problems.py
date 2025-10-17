'''
This script functions as the driver for the problem_generators module,
which creates generates randomized problems at various levels of difficulty for the domains we evaluate over.
'''

import os
import shutil
from typing import Any
from pathlib import Path

from nl3pddl.logger import logger

from .problem_generators import PROBLEM_GENERATORS

from nl3pddl.config import PLANS_PER_PROBLEM, NUM_EVAL_PROBLEMS, NUM_FEEDBACK_PROBLEMS

from kstar_planner.planners import plan_topk

GENERATED_PROBLEMS_DIR = "data/gen_problems"
FEEDBACK_PROBLEMS_DIR = os.path.join(GENERATED_PROBLEMS_DIR, "feedback")
EVAL_PROBLEMS_DIR = os.path.join(GENERATED_PROBLEMS_DIR, "evaluation")

def new_pipe(tmpdir : str, pipe_name : str, contents : str) -> str:
    """
    Creates a new pipe in the tempdir at tmpdir with filename,
    writes contents to the pipe, and returns a path to it.
    """
    pipe_path = os.path.join(tmpdir, pipe_name)
    with open(pipe_path, "w", encoding="utf-8") as pipe:
        pipe.write(contents)
    return pipe_path

def plan_file(domain_path : str, problem_path : str, k : int) \
-> dict[str, Any]:
    """
    Given a domain path and a problem invoke K* and produce k optimal plans as
    a json plans object.
    """
    result = plan_topk(
        domain_file=Path(domain_path),
        problem_file=Path(problem_path),
        number_of_plans_bound=k,
        timeout=60
    )

    # Check for errors
    if result.get("unsolvable"):
        print("No plan found for domain and problem (unsolvable)")
        return None

    if result.get("timeout_triggered"):
        print("No plan found for domain and problem due to timeout")
        return None

    if "planner_error" in result and result["planner_error"]:
        print(f"Planner error: {result['planner_error']}")
        return None

    if "plans" not in result or len(result["plans"]) == 0:
        print("No plans found")
        return None

    return result

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
        generator, 
        i, 
        problem_file, 
        domain_file
) -> dict[str, Any]: 
    while True:
        generator(i, problem_file)
        print(f"Generated {problem_file}")
        plans = plan_file(
            domain_file, problem_file, k=PLANS_PER_PROBLEM
        )
        if plans is None:
            logger.error(
                f"Failed to gen plans for {problem_file}, retrying..."
            )
            continue
        return plans

def generate_problems() -> None:
    if os.path.exists(GENERATED_PROBLEMS_DIR):
        shutil.rmtree(GENERATED_PROBLEMS_DIR)
    for domain_name, generator in PROBLEM_GENERATORS.items():
        domain_file = f"data/domains/{domain_name}/ground.pddl"
        assert os.path.exists(domain_file), \
            f"Domain file {domain_file} does not exist. " \
            "Please ensure the domain is generated first."
        #Create problems director if it doesn't exist
        feedback_problems_dir = os.path.join(FEEDBACK_PROBLEMS_DIR, domain_name)
        os.makedirs(feedback_problems_dir)
        # Generate NUM_PROBLEMS feedback problems for each domain
        for i in range(1, NUM_FEEDBACK_PROBLEMS + 1):
            problem_file = os.path.join(
                feedback_problems_dir, 
                f"problem-{i}.pddl"
            )

            # Try generating a problem and plans on it, fail if impossible
            plans = gen_problem_till_success(generator, i, problem_file, domain_file)

            plans = plans["plans"]
            # assert len(plans) == PLANS_PER_PROBLEM, \
            #     f"Expected {PLANS_PER_PROBLEM} plans, got {len(plans)} for {problem_file}"
            for j, plan in enumerate(plans):
                print(f"Generated plan for {problem_file}: {plan}")
                plan_str = plan_to_string(plan)
                plan_path = os.path.join(
                    feedback_problems_dir, 
                    f"plan-{i}-{j}.txt"
                )
                with open(plan_path, 'w', encoding='utf-8') as file:
                    file.write(plan_str)
        # Create evaluation problems directory
        evaluation_problems_dir = os.path.join(EVAL_PROBLEMS_DIR, domain_name)
        os.makedirs(evaluation_problems_dir, exist_ok=True)
        for i in range(1, NUM_EVAL_PROBLEMS + 1):
            problem_file = os.path.join(evaluation_problems_dir, f"problem-{i}.pddl")
            # Generate the top 2 plans for each problem
            plans = gen_problem_till_success(
                generator, i, problem_file, domain_file
            )
            plans = plans["plans"]
            # assert len(plans) == PLANS_PER_PROBLEM, \
            #     f"Expected {PLANS_PER_PROBLEM} plans, got {len(plans)} for {problem_file}"
            for j, plan in enumerate(plans):
                if len(plan["actions"]) == 0:
                    print(f"No actions in plan for {problem_file}, skipping")
                    continue
                print(f"Generated plan for {problem_file}: {plan}")
                plan_str = plan_to_string(plan)
                plan_path = os.path.join(
                    evaluation_problems_dir, 
                    f"plan-{i}-{j}.txt"
                )
                with open(plan_path, 'w', encoding='utf-8') as file:
                    file.write(plan_str)