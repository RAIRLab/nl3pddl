
"""
This file provides a class wrapping the top level experimental parameters,
as well as a function that generates a grid over these parameters.
"""

from dataclasses import dataclass
from typing import Generator

from .dataset import Dataset

MODELS = {
    "openai" : {
        "gpt-4o-mini"
    },
    "deepseek" : {
        "deepseek-chat", "deepseek-reasoner"
    }
}

GIVE_PRED_DESCRIPTIONS = [True]

DESC_CLASSES = [
    "detailed-first", "first"
]


@dataclass
class Params:
    domain_path : str
    provider : str
    model : str
    give_pred_descriptions : bool
    desc_class : str

def param_grid(d : Dataset) -> Generator[Params, None, None]:
    for provider in MODELS.keys():
        for model_name in MODELS[provider]:
            for domain_path in d.domain_paths:
                for give_pred_desc in GIVE_PRED_DESCRIPTIONS:
                    for desc_class in DESC_CLASSES:
                        yield Params(domain_path, provider, model_name, give_pred_desc, desc_class)


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