
"""
Adapted from the original NL2PDDL code
"""

#Standard Libs
import sqlite3
import os
import sys
import json
import shutil
import tempfile
import subprocess
from typing import Any
from subprocess import CalledProcessError

#The location of VAL relative to where this is being run from
VAL_PATH = "VAL/build/bin/Validate"

def new_pipe(tmpdir : str, pipe_name : str, contents : str) -> str:
    """
    Creates a new pipe in the tempdir at tmpdir with filename,
    writes contents to the pipe, and returns a path to it.
    """
    pipe_path = os.path.join(tmpdir, pipe_name)
    with open(pipe_path, "w", encoding="utf-8") as pipe:
        pipe.write(contents)
    return pipe_path

def plan_to_string(plan_obj : dict[str, Any]) -> str:
    """
    Return a VAL parsable plan from json object output by K*
    """
    plan_actions = plan_obj["actions"]
    result_plan_string : str = ""
    for action_str in plan_actions:
        result_plan_string += "(" + action_str + ")\n"
    return result_plan_string

def validate(domain_path : str, problem_path : str, plan : str) \
-> tuple[bool, str]:
    """
    Validate a plan on a domain and problem, returns a tuple of
    a boolean indicating if the plan is valid and a string
    containing an error message if the plan is invalid.
    """
    tmpdir = tempfile.mkdtemp()
    new_plan_path = new_pipe(tmpdir, 'new_plan.pddl', plan)
    try:
        #Forward direction, try plan from the new domain in the original domain
        args = [VAL_PATH, domain_path, problem_path, new_plan_path]
        _ = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        shutil.rmtree(tmpdir)
        return True, ""
    except CalledProcessError as err:
        shutil.rmtree(tmpdir)
        return False, err.output.decode()


def can_apply_plan(
    original_domain_path : str, new_domain : str,
    problem_path : str,
    original_plan : str, new_plan : str,
) -> tuple[bool, str, str, str]:
    """
    Given an original domain (path) and a new domain (string) problem,
    check if the the plan from the original can be used in
    the new domain and vice versa.
    """
    tmpdir = tempfile.mkdtemp()
    new_domain_path = new_pipe(tmpdir, 'new_domain.pddl', new_domain)
    new_plan_path = new_pipe(tmpdir, 'new_plan.pddl', new_plan)
    original_plan_path = new_pipe(tmpdir, 'original_plan.pddl', original_plan)
    try:
        #Forward direction, try plan from the new domain in the original domain
        args = [VAL_PATH, original_domain_path, problem_path, new_plan_path]
        _ = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    except CalledProcessError as err:
        shutil.rmtree(tmpdir)
        return False, "DifDomain", "NewToOriginal", err.output.decode()
    try:
        #Backward direction, try plan from the original domain in the new domain
        args = [VAL_PATH, new_domain_path, problem_path, original_plan_path]
        _ = subprocess.check_output(args, stderr=subprocess.DEVNULL)
    except CalledProcessError as err:
        shutil.rmtree(tmpdir)
        return False, "DifDomain", "OriginalToNew", err.output.decode()
    shutil.rmtree(tmpdir)
    if os.path.exists("found_plans"):
        shutil.rmtree("found_plans")
    return True, "EqDomain", "", ""

def evaluate_responses(conn : sqlite3.Connection, loop_id : int) -> None:
    """
    Loop through all available requests at a given loop_id and get the responses from the OpenAI API.
    """
    cursor = conn.cursor()
    requests = cursor.execute("""
        SELECT pl.plan_file, p.problem_file, d.name, r.raw_response
        FROM ModelResponses WHERE loop_id = ? and error = 0 
    """, (loop_id,)).fetchall()
    for ()