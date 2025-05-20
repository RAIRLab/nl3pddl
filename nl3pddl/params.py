
"""
This file provides a class wrapping the top level experimental parameters,
as well as a function that generates a grid over these parameters.
"""

from dataclasses import dataclass
from typing import Generator

from .dataset import Dataset

MODELS = {
    "openai" : {
        "o4-mini", "gpt-4o-mini"
    },
    "deepseek" : {
        "deepseek-chat"
    }
}

GIVE_PRED_DESCRIPTIONS = [True]

DESC_CLASSES = [
    "detailed-first", "first"
]

RUN_TRIALS = 3


@dataclass
class Params:
    domain_path : str
    provider : str
    model : str
    give_pred_descriptions : bool
    desc_class : str
    trial : int

def param_grid(d : Dataset) -> Generator[Params, None, None]:
    for trial in range(1, RUN_TRIALS + 1):
        for provider in MODELS.keys():
            for model_name in MODELS[provider]:
                for domain_path in d.domain_paths:
                    for give_pred_desc in GIVE_PRED_DESCRIPTIONS:
                        for desc_class in DESC_CLASSES:
                            yield Params(domain_path, provider, model_name, give_pred_desc, desc_class, trial)


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

def params_as_dict(p : Params, hde_runs: int, action_runs : int) -> dict:
    """
    Returns the parameters as a dictionary
    """
    return {
        "trial": p.trial,
        "domain_path": p.domain_path,
        "provider": p.provider,
        "model": p.model,
        "give_pred_descriptions": p.give_pred_descriptions,
        "desc_class": p.desc_class,
        "hde_runs" : hde_runs,
        "action_runs" : action_runs
    }

def params_header () -> list[str]:
    """
    Returns the header for the parameters
    """
    return ["trial", "domain_path", "provider", "model", "give_pred_descriptions", "desc_class", "hde_runs", "action_runs"]