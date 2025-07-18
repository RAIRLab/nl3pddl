
"""
This file contains the global logger for the NL3PDDL project.
"""

import logging

import yaml

with open("experiment_config.yaml", "r") as f:
    config = yaml.safe_load(f)

LOG_LEVEL = config["log-level"]

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)