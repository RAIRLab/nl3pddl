"""
Wrapper for the VAL validator
"""

import os
import shutil
import tempfile
import subprocess
from subprocess import CalledProcessError

from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from .dataset import PipelineResult, Dataset
from .params import Params

#The location of VAL relative to where this is being run from
VAL_PATH = "submodules/VAL/build/bin/Validate"

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
    Given an original domain (path) and a new domain (string) problem,
    check if the the plan from the original can be used in
    the new domain. returns None if the plan is valid in the new domain,
    or an error message if it is not valid.
    """
    tmpdir = tempfile.mkdtemp()
    new_domain_path = new_pipe(tmpdir, 'new_domain.pddl', new_domain_str)
    try:
        #Forward direction, try plan from the new domain in the original domain
        args = [VAL_PATH, "-v", "-e", new_domain_path, problem_path, plan_path]
        _ = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    except CalledProcessError as err:
        shutil.rmtree(tmpdir)
        return err.output.decode()
    shutil.rmtree(tmpdir)
    if os.path.exists("found_plans"):
        shutil.rmtree("found_plans")
    return None

def raw_antivalidate(
    new_domain_str : str,
    problem_path : str,
    wplan_path : str
) -> str | None:
    """
    Validates that the new domain against a wrong plan,
    expects validation failure. 
    TODO: Needs better error messages based on generation of wrong plants
    that specify where the error is in the plan.
    """
    res = raw_validate(new_domain_str, problem_path, wplan_path)
    if res is None:
        return "Validation of wrong plan in new domain succeeded, \
        but it should not have."
    return None

VAL_PROMPT_TEMPLATE = PromptTemplate.from_file("data/prompts/9-val.txt")
VALW_PROMPT_TEMPLATE = PromptTemplate.from_file("data/prompts/10-valw.txt")

def val_feedback(d : Dataset, p : Params, new_domain_str : str) ->\
HumanMessage | None:
    """
    Check if the new domain is valid for all problems and plans, if not, 
    return an error message with the problem and plan that failed validation, as well as the error message from VAL.
    """
    # Get the domain and problem paths
    problem_paths = d.feedback_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        for plan_path in d.feedback_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is not None:
                problem_raw = d.feedback_problem_raws[problem_path]
                plan_raw = d.feedback_plan_raws[plan_path]
                return HumanMessage(VAL_PROMPT_TEMPLATE.format(
                    problem=problem_raw,
                    plan=plan_raw,
                    val_output=result
                ))
    return None

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
        for plan_path in d.evaluation_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is None:
                valid_count += 1
            total_count += 1
    return valid_count, total_count
