"""
    Simple utility to build PDDL problem files for the 'sudoku' domain.
"""

import random

def generate_sudoku_problem(output_file, seed=None):

    grid_size = 4

    if (seed is not None):
        random.seed(seed)

    digits = [1, 2, 3, 4]
    positions = [f"r{r}c{c}" for r in range(1, grid_size + 1) for c in range(1, grid_size + 1)]
    
    # Start with all zeros
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Randomly place one of each digit in unique cells
    used_positions = random.sample(positions, len(digits))
    for pos, digit in zip(used_positions, digits):
        r = int(pos[1]) - 1
        c = int(pos[3]) - 1
        grid[r][c] = digit

    # PDDL problem text
    problem = f"(define (problem sudoku)\n"
    problem += "  (:domain sudoku-4x4)\n"
    
    # Declare objects
    problem += "  (:objects\n"
    problem += "    " + " ".join(positions) + " - cell\n"
    problem += "    one two three four - number\n"
    problem += "  )\n\n"

    # Initial states
    problem += "  (:init\n"

    # Encode pre-filled cells
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] != 0:
                num = ["one", "two", "three", "four"][grid[r][c]-1]
                problem += f"    (filled r{r+1}c{c+1} {num})\n"
    problem += "  )\n\n"

    # Goal
    problem += "  (:goal (and\n"
    for pos in positions:
        problem += f"    (exists (?n - number) (filled {pos} ?n))\n"
    problem += "  ))\n"
    problem += ")"
    
    return problem

    with open(output_file, "w") as f:
        f.write(problem)