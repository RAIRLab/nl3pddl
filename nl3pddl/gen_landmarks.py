
# This script generates landmark json for each problem in the domain

import os
import subprocess
import json
import glob
import re
from forbiditerative import planners
from pathlib import Path

import matplotlib.pyplot as plt

import pddl

from .config import DOMAINS
from nl3pddl.utils import grounded_pred_to_lm_str

# Define paths
DOMAINS_PATH = "data/domains"
PROBLEMS_PATH = "data/gen_problems/feedback"
OUTPUT_DIR = "data/gen_landmarks"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_pddl_domain_name(domain_file: str) -> str:
    """Parse PDDL to get the domain name string."""
    try:
        dom = pddl.parse_domain(domain_file)
        return dom.name
    except Exception as e:  # pylint: disable=broad-except
        # Fallback to folder name if parsing fails
        print(f"Warning: failed to parse domain name from {domain_file}: {e}")
        return os.path.basename(os.path.dirname(domain_file))

# Generates landmarks in the form of {"facts": ["Atom ontable(b2)"], "disjunctive": "False", "first_achievers": ["put-down b2"]}
def generate_landmarks_for(domain_file, problem_file) -> dict:
    try:
        domain_path = Path(domain_file)
        problem_path = Path(problem_file)
        # Get exhaustive landmarks using the built-in landmark method
        landmarks = planners.get_landmarks(
            domain_file=domain_path, 
            problem_file=problem_path, 
            method='exhaust'
        )
        return landmarks
    except Exception as e:
        print(f"Error generating landmarks for {problem_file}: {e}")
        raise

def gen_action_landmarks(landmarks : list[dict]):
    # For each item in landmarks, read the first_achievers, discard the objects, and create a tuple of all first_achievers, and the set of all of these is the action landmarks for a given domain/problem pair
    action_landmarks = set()
    for item in landmarks:
        first_achievers = item.get('first_achievers', [])
        actions = tuple(set(achiever for achiever in first_achievers))
        action_landmarks.add(actions)
    return action_landmarks
    

def generate_landmarks():
    """Generates landmarks for all domains and problems in the specified directories.
    """
    # Find all domain and problem files
    all_data = []
    domain_files = [os.path.join(DOMAINS_PATH, domain, "ground.pddl") for domain in DOMAINS]

    for domain_file in domain_files:
        domain_name = extract_pddl_domain_name(domain_file)
        # Look for problems like problem-1.pddl, problem-2.pddl, problem-3.pddl, etc.
        problem_pattern = os.path.join(PROBLEMS_PATH, domain_name, "problem-*.pddl")
        problem_files = glob.glob(problem_pattern)
        
        # If still no problems found, print a warning
        if not problem_files:
            print(f"Warning: No problem files found for domain {domain_name}")
        
        print(f"Processing domain: {domain_name} with {len(problem_files)} problems")
        # Create output directory for the domain if it doesn't exist
        os.makedirs(f"{OUTPUT_DIR}/{domain_name}", exist_ok=True)

        #Wipe the directory files
        for file in glob.glob(f"{OUTPUT_DIR}/{domain_name}/*"):
            os.remove(file)

        # Generate landmarks for each problem file
        for problem_file in problem_files:
            problem_name = os.path.basename(problem_file)
            problem_num = int(re.search(r'problem-(\d+)', problem_name).group(1))
            output_file = f"{OUTPUT_DIR}/{domain_name}/{problem_name.replace('.pddl', '.json')}"

            success = generate_landmarks_for(domain_file, problem_file)

            # Filter landmarks into three classes 
            # trivial, where the landmark is in the initial state
            # non-trivial, where the landmark is not in the initial state
            # non-applicable, where the landmark is a negated atom or
            # special value, <none of those>
            problem_object = pddl.parse_problem(problem_file) 
            initial_state = set(str(atom) for atom in problem_object.init)
            initial_state = {grounded_pred_to_lm_str(atom) for atom in problem_object.init}
            trivial_landmarks = []
            non_applicable_landmarks = []
            non_trivial_landmarks = []
            for lm in success['landmarks']:
                lm_str = str(lm["facts"][0])
                if lm_str in initial_state:
                    trivial_landmarks.append(lm)
                elif "NegatedAtom" in lm_str or "<none of those>" in lm_str:
                    non_applicable_landmarks.append(lm)
                else:
                    non_trivial_landmarks.append(lm)

            # Write the landmarks
            json.dump({
                'domain': domain_name,
                'problem': problem_name,
                'problem_num': problem_num,
                'trivial_state_landmarks': [lm["facts"][0] for lm in trivial_landmarks],
                'non_trivial_state_landmarks': [lm["facts"][0] for lm in non_trivial_landmarks],
                'non_applicable_state_landmarks': [lm["facts"][0] for lm in non_applicable_landmarks],
                'landmarks': list(gen_action_landmarks(non_trivial_landmarks)),
                'raw_output': success
            }, open(output_file, 'w'), indent=4)
    
