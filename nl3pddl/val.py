
import os
import shutil
import tempfile
import subprocess
from typing import Any
from subprocess import CalledProcessError
from dataclasses import dataclass

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
) -> PipelineResult:
    """
    Given an original domain (path) and a new domain (string) problem,
    check if the the plan from the original can be used in
    the new domain and vice versa.
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


val_prompt_template = PromptTemplate(template="""
    Given the above domain you just generated, attempting to use it with the following problem:
    ```
    {problem}
    ```
    An issue was encountered with the following plan:
    ```
    {plan}
    ```
    The output of the plan validator VAL is:
    ```
    {val_output}
    ```
    Please revise the pervious domain to fix the issue. 
    You may create new predicates and types if needed, but make
    sure to update the predicate and type lists accordingly.
    You may not add new requirements to the domain,
    your output should exclusively be a typed STRIPS domain.
""")

def val_all(d : Dataset, p : Params, new_domain_str : str) -> HumanMessage | None:
    """
    Check if the new domain is valid for all problems and plans
    """
    # Get the domain and problem paths
    problem_paths = d.problem_paths[p.domain_path]
    for problem_path in problem_paths:
        plan_path = d.plan_paths[problem_path]
        # Validate the new domain
        result = raw_validate(new_domain_str, problem_path, plan_path)
        if result is not None:
            problem_raw = d.problem_raws[problem_path]
            plan_raw = d.plan_raws[plan_path]
            return HumanMessage(val_prompt_template.format(
                problem=problem_raw,
                plan=plan_raw,
                val_output=result
            ))
    return None
