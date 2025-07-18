
"""
This file provides a class wrapping the top level experimental parameters,
as well as a function that generates a grid over these parameters.
"""

from dataclasses import dataclass
from typing import Generator

from .dataset import Dataset

import yaml

with open("experiment_config.yaml", "r") as f:
    config = yaml.safe_load(f)

RUN_TRIALS = config["trials"]
ACTION_THRESHOLD = config["action-threshold"]
HDE_THRESHOLD = config["hde-threshold"]
KSTAR_TIMEOUT = config["kstar-timeout"]
MODELS = config["models"]
GIVE_PRED_DESCRIPTIONS = config["give-pred-description"]
DESC_CLASSES = config["description-classes"]


@dataclass
class Params:
    """
    This class contains the parameters for a single experiment run.
    It is distinct from the Dataset class, which contains the fixed dataset
    used by all experiments, but does contain some flags specifying what 
    parts of the dataset should be used, i.e. what description class etc.
    """
    domain_path : str
    provider : str
    model : str
    give_pred_descriptions : bool
    desc_class : str
    trial : int

def param_grid(d : Dataset) -> Generator[Params, None, None]:
    """
    Generates a grid of parameters for the experiments.
    """
    for trial in range(1, RUN_TRIALS + 1):
        for provider, models in MODELS.items():
            for model in models:
                for domain_path in d.domain_paths:
                    for give_pred_desc in GIVE_PRED_DESCRIPTIONS:
                        for desc_class in DESC_CLASSES:
                            yield Params(
                                domain_path, provider, model,
                                give_pred_desc, desc_class, trial
                            )


def action_names(d : Dataset, h : Params) -> list[str]:
    """
    Returns a list of action names in the domain
    """
    return list(d.nl_json[h.domain_path]["actions"].keys())

def domain_name(d : Dataset, h : Params) -> str:
    """
    Returns the name of the domain
    """
    return d.domains[h.domain_path].name

def get_hde_iteration_threshold() -> int:
    """
    Returns the HDE iteration threshold for the experiment.
    """
    return HDE_THRESHOLD

def get_action_iteration_threshold() -> int:
    """
    Returns the action iteration threshold for the experiment.
    """
    return ACTION_THRESHOLD