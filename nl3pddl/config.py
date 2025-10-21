
import os
import sys
from pathlib import Path

import yaml

# Check if config file is specified in command line args
config_file = "experiment_config.yaml"
for i, arg in enumerate(sys.argv):
    if arg in ["-c", "--config"] and i + 1 < len(sys.argv):
        config_file = sys.argv[i + 1]
        break

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

NUM_FEEDBACK_PROBLEMS = config["feedback-problems"]
NUM_EVAL_PROBLEMS = config["evaluation-problems"]
PLANS_PER_PROBLEM = config["plans-per-problem"]

LOG_LEVEL : int = config["log-level"]
RUN_TRIALS : int = config["trials"]
ACTION_THRESHOLD : int = config["action-threshold"]
HDE_THRESHOLD : int = config["hde-threshold"]
KSTAR_TIMEOUT : float = config["kstar-timeout"]
THREADS : int = config["threads"]
KSTAR_N_PLANS : int = config["kstar-n-plans"]

MODELS : dict[str, list[str]] = config["models"]
GIVE_PRED_DESCRIPTIONS : list[bool] = config["give-pred-description"]
assert 1 <= len(GIVE_PRED_DESCRIPTIONS) <= 2, \
    "give-pred-description can only be a list of length 1 or 2"
DESC_CLASSES : list[str] = config["description-classes"]
FEEDBACK_PIPELINES : list[list[str]] = config["feedback-pipelines"]
SEARCH_HEURISTICS : list[str] = config["search-heuristic"]

# Hardcoded paths
PROMPT_DIR = "data/prompts"
GENERATED_PROBLEMS_DIR : Path = "data/gen_problems"
FEEDBACK_PROBLEMS_DIR : Path = os.path.join(GENERATED_PROBLEMS_DIR, "feedback")
EVAL_PROBLEMS_DIR : Path = os.path.join(GENERATED_PROBLEMS_DIR, "evaluation")