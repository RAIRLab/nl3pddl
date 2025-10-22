"""
This file contains the main functions for generating feedback prompts
and evaluating the results of a model. 
"""

import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from subprocess import CalledProcessError

from kstar_planner import planners
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from nl3pddl.params import Params
from nl3pddl.logger import logger
from nl3pddl.dataset import Dataset
from nl3pddl.config import KSTAR_N_PLANS, KSTAR_TIMEOUT

#The location of VAL relative to where this is being run from
VAL_PATH = "submodules/VAL/build/bin/Validate"

VAL_PROMPT_TEMPLATE = PromptTemplate.from_file("data/prompts/9-val.txt")
VALW_PROMPT_TEMPLATE = PromptTemplate.from_file("data/prompts/10-valw.txt")
LANDMARK_PROMPT_TEMPLATE = \
    PromptTemplate.from_file("data/prompts/11-landmarks.txt")
UNSOLVABLE_PROMPT_TEMPLATE = \
    PromptTemplate.from_file("data/prompts/12-unsolvable.txt")

def new_pipe(tmpdir : str, pipe_name : str, contents : str) -> str:
    """
    Creates a new pipe in the tempdir at tmpdir with filename,
    writes contents to the pipe, and returns a path to it.
    """
    pipe_path = os.path.join(tmpdir, pipe_name)
    with open(pipe_path, "w", encoding="utf-8") as pipe:
        pipe.write(contents)
    return pipe_path

def raw_validate(
    new_domain_str : str,
    problem_path : str,
    plan_path : str
) -> str | None:
    """
    Given a domain string (presumably produced by the model), a problem path,
    and a plan path, validates the plan against the problem in the new domain.
    """
    tmpdir = tempfile.mkdtemp()
    new_domain_path = new_pipe(tmpdir, 'new_domain.pddl', new_domain_str)
    try:
        #Forward direction, try plan from the new domain in the original domain
        args = [VAL_PATH, "-v", "-e", new_domain_path, problem_path, plan_path]
        _ = subprocess.check_output(args)
    except CalledProcessError as err:
        shutil.rmtree(tmpdir)
        stdoutstr = err.output.decode() if err.output else "No STDOUT"
        stderrstr = err.stderr.decode() if err.stderr else "No STDERR"
        if err.returncode == -11:
            return "The PDDL for the generated domain is invalid, and caused val to crash. Please ensure it is valid STRIPS style PDDL. Check to ensure that the typing is correct."
        if err.returncode == 1:
            # It is imperative we return the stderr here, as VAL outputs nothing on stdout on plan check failure.
            return "VAL Failed to execute the plan: " + stderrstr
        return "VAL Failed with the following outputs STDOUT:\n" + stdoutstr + "\nSTDERR:\n" + stderrstr
    shutil.rmtree(tmpdir)
    # if os.path.exists("found_plans"):
    #     shutil.rmtree("found_plans")
    return None

#TODO: consider removing.
# def single_val_feedback(d : Dataset, p : Params, new_domain_str : str) ->\
# HumanMessage | None:
#     """
#     Check if the new domain is valid for all problems and plans, if not, 
#     return an error message with the problem and plan that failed validation, as well as the error message from VAL.
#     """
#     # Get the domain and problem paths
#     problem_paths = d.feedback_problem_paths[p.domain_path]
#     for problem_path in problem_paths:
#         for plan_path in d.feedback_plan_paths[problem_path]:
#             result = raw_validate(new_domain_str, problem_path, plan_path)
#             if result is not None and (result == "" or result.strip()) == "":
#                 result = "The PDDL for the generated domain is invalid, and caused val to crash. Please ensure it is valid STRIPS style PDDL."
#             if result is not None:
#                 problem_raw = d.feedback_problem_raws[problem_path]
#                 plan_raw = d.feedback_plan_raws[plan_path]
#                 return HumanMessage(VAL_PROMPT_TEMPLATE.format(
#                     problem=problem_raw,
#                     plan=plan_raw,
#                     val_output=result
#                 ))
#     return None

def val_evaluate(
        d : Dataset, 
        p : Params,
        new_domain_str : str
) -> tuple[int, int]:
    """
    Checks how many plans are valid in the new domain from the evaluation set.
    """
    valid_count = 0
    total_count = 0
    # Get the evaluation problem paths
    problem_paths = d.evaluation_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        problem_valid = True
        # If any of the plans for the problem fail, report it as the
        # problem failing HDE
        for plan_path in d.evaluation_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is None:
                continue
            problem_valid = False
        if problem_valid:
            valid_count += 1
        total_count += 1
    return valid_count, total_count

def raw_kstar(
    new_domain_str : str,
    problem_path : str
) -> dict | None:
    tmpdir = tempfile.mkdtemp()
    new_domain_path = new_pipe(tmpdir, 'new_domain.pddl', new_domain_str)
    plans = planners.plan_topk(
        domain_file=Path(new_domain_path), 
        problem_file=Path(problem_path), 
        number_of_plans_bound=KSTAR_N_PLANS, 
        timeout=KSTAR_TIMEOUT
    )
    return plans

def single_landmark_feedback(
    d : Dataset, 
    p : Params, 
    new_domain_str : str
) -> HumanMessage | None:
    """
    Checks if the new domain when a creating a plan with the original problem, 
    satisfied the original domain's landmarks for that problem. If the new domain is incompatible with the problem files, or the plan satisfies the landmarks returns None, otherwise if the landmarks are not satisfied, returns a message with the problem, landmark that was not satisfied.
    """
    # Get the new domain's landmarks
    problem_paths = d.feedback_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        landmarks = d.landmarks[problem_path]
        plan_obj = raw_kstar(new_domain_str, problem_path)
        if plan_obj is None:
            continue
        if plan_obj["unsolvable"]:
            return HumanMessage(
                UNSOLVABLE_PROMPT_TEMPLATE.format(
                    problem=d.feedback_problem_raws[problem_path]
                )
            )
        if not plan_obj["plans"] or len(plan_obj["plans"]) == 0:
            logger.warning(
                "No plans generated for problem %s in domain %s",
                problem_path, p.domain_path
            )
            continue
        new_plans = plan_obj["plans"]
        for new_plan in new_plans:
            # By dumping the plan to a string, we can check if an action is satisfied just by checking if the action is in the string.
            new_plan_str = "\n".join(f"({a})" for a in new_plan["actions"])
            for landmark in landmarks:
                landmark_str = "\n".join([f"({l})" for l in landmark])
                landmark_satisfied = False
                for landmark_disjunt in landmark:
                    if landmark_disjunt in new_plan_str:
                        landmark_satisfied = True
                        break
                if not landmark_satisfied:
                    problem_raw = d.feedback_problem_raws[problem_path]
                    return HumanMessage(LANDMARK_PROMPT_TEMPLATE.format(
                        problem=problem_raw,
                        landmark=landmark_str,
                        plan=new_plan_str
                    ))
    return None

def multi_val_feedback(d : Dataset, p : Params, new_domain_str : str) ->\
list[HumanMessage]:
    """
    Check if the new domain is valid for all problems and plans, returns
    ALL error messages with the problem and plan that failed validation, as well as the error message from VAL.
    """
    # Get the domain and problem paths
    problem_paths = d.feedback_problem_paths[p.domain_path]
    results = []
    for problem_path in problem_paths:
        for plan_path in d.feedback_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is not None:
                problem_raw = d.feedback_problem_raws[problem_path]
                plan_raw = d.feedback_plan_raws[plan_path]
                results.append(HumanMessage(VAL_PROMPT_TEMPLATE.format(
                    problem=problem_raw,
                    plan=plan_raw,
                    val_output=result
                )))
    return results

def multi_landmark_feedback(
    d : Dataset, 
    p : Params, 
    new_domain_str : str
) -> list[HumanMessage] | None:
    """
    Version of single_landmark_feedback that returns ALL unsatisfied landmarks, not just the first one found.
    """
    results = []
    # Get the new domain's landmarks
    problem_paths = d.feedback_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        landmarks = d.landmarks[problem_path]
        plan_obj = raw_kstar(new_domain_str, problem_path)
        if plan_obj is None:
            continue
        if plan_obj["unsolvable"]:
            results.append(HumanMessage(
                UNSOLVABLE_PROMPT_TEMPLATE.format(
                    problem=d.feedback_problem_raws[problem_path]
                )
            ))
        if not plan_obj["plans"] or len(plan_obj["plans"]) == 0:
            logger.warning(
                "No plans generated for problem %s in domain %s",
                problem_path, p.domain_path
            )
            continue
        new_plans = plan_obj["plans"]
        for new_plan in new_plans:
            # By dumping the plan to a string, we can check if an action is satisfied just by checking if the action is in the string.
            new_plan_str = "\n".join(f"({a})" for a in new_plan["actions"])
            for landmark in landmarks:
                landmark_str = "\n".join([f"({l})" for l in landmark])
                landmark_satisfied = False
                for landmark_disjunt in landmark:
                    if landmark_disjunt in new_plan_str:
                        landmark_satisfied = True
                        break
                if not landmark_satisfied:
                    problem_raw = d.feedback_problem_raws[problem_path]
                    results.append(HumanMessage(LANDMARK_PROMPT_TEMPLATE.format(
                        problem=problem_raw,
                        landmark=landmark_str,
                        plan=new_plan_str
                    )))
    return results

def val_feedback_test(
        d : Dataset, 
        p : Params,
        new_domain_str : str
) -> tuple[int, int]:
    """
    Checks how many plans are valid in the new domain from the evaluation set.
    """
    valid_count = 0
    total_count = 0
    # Get the evaluation problem paths
    problem_paths = d.feedback_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        problem_valid = True
        # If any of the plans for the problem fail, report it as the
        # problem failing HDE
        for plan_path in d.feedback_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is None:
                continue
            problem_valid = False
        if problem_valid:
            valid_count += 1
        total_count += 1
    return valid_count, total_count