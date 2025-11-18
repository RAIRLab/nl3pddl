from typing import Callable, Any

from .blocks import generate_problem as generate_blocks_problem
from .checkers import generate_problem as generate_checkers_problem
from .elevators import generate_problem as generate_elevators_problem
from .flow import generate_problem as generate_flow_problem
from .bookseller import generate_problem as generate_bookseller_problem
from .hiking import generate_hiking_problem
from .keygrid import generate_keygrid_problem
from .pacman_63 import generate_pacman_63_problem
from .pacman_72 import generate_pacman_problem
from .sliding_puzzle import generate_sliding_puzzle_problem
from .lightBubble import generate_problem as generate_light_bubble_problem
from .sudoku import generate_sudoku_problem
from .hanoi import generate_hanoi_problem as generate_hanoi_problem
from .bloxorz_maze_generator import generate_bloxorz_problem
from .sudoku_9x9 import generate_sudoku_9x9_problem

# GENS is a dictionary mapping problem names to their respective generation functions.
# DO NOT COMMENT OUT GENERATORS HERE; instead, modify the experiment_config.yaml to include/exclude domains.
PROBLEM_GENERATORS : dict[str, Callable[[Any], None]] = {
    "blocks": generate_blocks_problem,
    "checkers-jumping": generate_checkers_problem,
    "miconic": generate_elevators_problem,
    "flow": generate_flow_problem,
    "bookseller": generate_bookseller_problem,
    "hiking": generate_hiking_problem,
    "keygrid": generate_keygrid_problem,
    "pacman-63": generate_pacman_63_problem,
    "pacman-72": generate_pacman_problem,
    "sliding-puzzle": generate_sliding_puzzle_problem,
    "light-bubble": generate_light_bubble_problem,
    "sudoku": generate_sudoku_problem,
    "hanoi" : generate_hanoi_problem,
    "bloxorz": generate_bloxorz_problem,
    "sudoku-9x9": generate_sudoku_9x9_problem
}
