from typing import Callable, Any

from .blocks import generate_problem as generate_blocks_problem
from .checkers import generate_problem as generate_checkers_problem
from .elevators import generate_problem as generate_elevators_problem
from .flow import generate_problem as generate_flow_problem
from .bookseller import generate_problem as generate_bookseller_problem

# GENS is a dictionary mapping problem names to their respective generation functions.
PROBLEM_GENERATORS : dict[str, Callable[[Any], None]] = {
    "blocks": generate_blocks_problem,
    "checkers-jumping": generate_checkers_problem,
    "miconic": generate_elevators_problem,
    "flow": generate_flow_problem,
    "bookseller": generate_bookseller_problem
}