
"""
This file contains the global logger for the NL3PDDL project.
"""

import logging

from nl3pddl.config import LOG_LEVEL

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)