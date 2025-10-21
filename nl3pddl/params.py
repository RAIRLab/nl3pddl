
"""
This file reads the config file and 
provides a class wrapping the top level experimental parameters,
as well as a function that generates a grid over these parameters,
and some utility functions for the params.
"""

from typing import Generator
from dataclasses import dataclass, field

from nl3pddl.dataset import Dataset
from nl3pddl.config import DESC_CLASSES, FEEDBACK_PIPELINES, GIVE_PRED_DESCRIPTIONS, MODELS, RUN_TRIALS, SEARCH_HEURISTICS

@dataclass
class Params:
    """
    This class contains the parameters for a single experiment run.
    It is distinct from the Dataset class, which contains the fixed dataset
    used by all experiments, but does contain some flags specifying what 
    parts of the dataset should be used, i.e. what description class etc.
    Default values are provided to create a dummy Params object.
    """
    domain_path : str               = ""
    provider : str                  = "openai"
    model : str                     = "gpt-5-nano"
    give_pred_descriptions : bool   = True
    desc_class : str                = ""
    trial : int                     = 1
    feedback_pipeline : list[str]   = field(default_factory=lambda: [])
    search_heuristic : str          = "G + H" # One of SEARCH_HEURISTICS

#TODO: please god put this in an itertools thing somehow.
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
                            for feedback_pipeline in FEEDBACK_PIPELINES:
                                # Skip heuristics for none and random-single pipelines
                                if feedback_pipeline == [] or "random-single" in feedback_pipeline:
                                    yield Params(
                                        domain_path,
                                        provider, model,
                                        give_pred_desc,
                                        desc_class,
                                        trial,
                                        feedback_pipeline,
                                        "G"
                                    )
                                else:
                                    for search_heuristic in SEARCH_HEURISTICS:
                                        yield Params(
                                            domain_path,
                                            provider, model,
                                            give_pred_desc,
                                            desc_class,
                                            trial,
                                            feedback_pipeline,
                                            search_heuristic
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

def feedback_pipeline_str(p : Params) -> str:
    """
    Returns a string representation of the feedback pipeline.
    """
    return "-".join(p.feedback_pipeline)