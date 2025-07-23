
import yaml

with open("experiment_config.yaml", "r") as f:
    config = yaml.safe_load(f)

NUM_FEEDBACK_PROBLEMS = config["feedback-problems"]
NUM_EVAL_PROBLEMS = config["evaluation-problems"]
PLANS_PER_PROBLEM = config["plans-per-problem"]

LOG_LEVEL = config["log-level"]
RUN_TRIALS = config["trials"]
ACTION_THRESHOLD = config["action-threshold"]
HDE_THRESHOLD = config["hde-threshold"]
KSTAR_TIMEOUT = config["kstar-timeout"]
THREADS = config["threads"]
KSTAR_N_PLANS = config["kstar-n-plans"]

MODELS = config["models"]
GIVE_PRED_DESCRIPTIONS = config["give-pred-description"]
DESC_CLASSES = config["description-classes"]
FEEDBACK_PIPELINES = config["feedback-pipelines"]