
import os
import yaml
from pathlib import Path

with open("experiment_config.yaml", "r") as f:
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
GIVE_PRED_DESCRIPTIONS : bool = config["give-pred-description"]
DESC_CLASSES : list[str] = config["description-classes"]
FEEDBACK_PIPELINES : list[list[str]] = config["feedback-pipelines"]

# Hardcoded paths
GENERATED_PROBLEMS_DIR : Path = "data/gen_problems"
FEEDBACK_PROBLEMS_DIR : Path = os.path.join(GENERATED_PROBLEMS_DIR, "feedback")
EVAL_PROBLEMS_DIR : Path = os.path.join(GENERATED_PROBLEMS_DIR, "evaluation")