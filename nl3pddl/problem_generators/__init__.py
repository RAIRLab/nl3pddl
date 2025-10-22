from typing import Callable, Any

from .blocks import generate_problem as generate_blocks_problem
from .checkers import generate_problem as generate_checkers_problem
from .elevators import generate_problem as generate_elevators_problem
from .flow import generate_problem as generate_flow_problem
from .bookseller import generate_problem as generate_bookseller_problem
from .hiking import generate_hiking_problem
from .keygrid import generate_keygrid_problem
from .pacman_72 import generate_pacman_problem


# GENS is a dictionary mapping problem names to their respective generation functions.
PROBLEM_GENERATORS : dict[str, Callable[[Any], None]] = {
    "blocks": generate_blocks_problem,
    "checkers-jumping": generate_checkers_problem,
    "miconic": generate_elevators_problem,
    "flow": generate_flow_problem,
    "bookseller": generate_bookseller_problem,
    "hiking": generate_hiking_problem,
    "keygrid": generate_keygrid_problem,
    "pacman-63": generate_pacman_ai_problem,
    "pacman-72": generate_pacman_problem
}