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
) -> PipelineResult | None:
    """
    Given an original domain (path) and a new domain (string) problem,
    check if the the plan from the original can be used in
    the new domain.
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

#TODO: This needs to be reimplemented if used
# def val_pos(d : Dataset, p : Params, new_domain_str : str) ->\
# HumanMessage | None:
#     """ Check if the new domain is valid for a single problem and plan"""
#     # Get the domain and problem paths
#     problem_paths = d.problem_paths[p.domain_path]
#     for problem_path in problem_paths:
#         for 
#         plan_path = d.plan_paths[problem_path]
#         # Validate the new domain
#         result = raw_validate(new_domain_str, problem_path, plan_path)
#         if result is not None:
#             problem_raw = d.problem_raws[problem_path]
#             plan_raw = d.plan_raws[plan_path]
#             return HumanMessage(VAL_PROMPT_TEMPLATE.format(
#                 problem=problem_raw,
#                 plan=plan_raw,
#                 val_output=result
#             ))

# def val_neg(d : Dataset, p : Params, new_domain_str : str) ->\
# HumanMessage | None:
#     """
#     Check if the new domain is invalid for a single problem and plan
#     """
#     # Get the domain and problem paths
#     problem_paths = d.problem_paths[p.domain_path]
#     for problem_path in problem_paths:
#         wplan_path = d.wplan_paths[problem_path]
#         result = raw_antivalidate(new_domain_str, problem_path, wplan_path)
#         if result is not None:
#             problem_raw = d.problem_raws[problem_path]
#             wplan_raw = d.wplan_raws[wplan_path]
#             return HumanMessage(VALW_PROMPT_TEMPLATE.format(
#                 problem=problem_raw,
#                 plan=wplan_raw
#             ))

def val_all(d : Dataset, p : Params, new_domain_str : str) ->\
HumanMessage | None:
    """
    Check if the new domain is valid for all problems and plans
    """
    # Get the domain and problem paths
    problem_paths = d.testing_problem_paths[p.domain_path]
    for problem_path in problem_paths:
        for plan_path in d.testing_plan_paths[problem_path]:
            result = raw_validate(new_domain_str, problem_path, plan_path)
            if result is not None:
                problem_raw = d.testing_problem_raws[problem_path]
                plan_raw = d.testing_plan_raws[plan_path]
                return HumanMessage(VAL_PROMPT_TEMPLATE.format(
                    problem=problem_raw,
                    plan=plan_raw,
                    val_output=result
                ))
        #TODO: Rework for wrong plans
        # # Validate the new domain against the wrong plan
        # wplan_path = d.wplan_paths[problem_path]
        # result = raw_antivalidate(new_domain_str, problem_path, wplan_path)
        # if result is not None:
        #     problem_raw = d.problem_raws[problem_path]
        #     wplan_raw = d.wplan_raws[plan_path]
        #     return HumanMessage(VALW_PROMPT_TEMPLATE.format(
        #         problem=problem_raw,
        #         plan=wplan_raw
        #     ))
    return None
