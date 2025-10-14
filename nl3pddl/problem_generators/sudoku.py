"""
Simple utility to build PDDL problem files for the 'sudoku' domain.
"""

import random

def generate_sudoku_problem(output_file, seed=None):
    grid_size = 4

    if seed is not None:
        random.seed(seed)

    digits = [1, 2, 3, 4]
    num_names = ["one", "two", "three", "four"]
    positions = [f"r{r}c{c}" for r in range(1, grid_size + 1) for c in range(1, grid_size + 1)]

    # Start with all zeros (unfilled)
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Randomly place one of each digit in unique cells
    used_positions = random.sample(positions, len(digits))
    for pos, digit in zip(used_positions, digits):
        r = int(pos[1]) - 1
        c = int(pos[3]) - 1
        grid[r][c] = digit

    # PDDL problem text
    problem = f"(define (problem sudoku)\n"
    problem += "  (:domain sudoku)\n"
    
    # Declare objects
    problem += "  (:objects\n"
    problem += "    " + " ".join(positions) + " - cell\n"
    problem += "    one two three four - number\n"
    problem += "  )\n\n"

    # Initial states
    problem += "  (:init\n"

    # Mark all cells as empty or filled
    for r in range(grid_size):
        for c in range(grid_size):
            cell = f"r{r+1}c{c+1}"
            if grid[r][c] != 0:
                num = num_names[grid[r][c]-1]
                problem += f"    (filled {cell})\n"
                problem += f"    (has-value {cell} {num})\n"
            else:
                problem += f"    (empty {cell})\n"
                # Each empty cell starts with all "not-has-value"
                for num in num_names:
                    problem += f"    (not-has-value {cell} {num})\n"

    # no-conflict relations 
    for r in range(1, grid_size + 1):
        for c in range(1, grid_size + 1):
            cell = f"r{r}c{c}"
            for num in num_names:
                conflict = False
                # Check if this cell already has a conflicting assignment
                if grid[r-1][c-1] != 0 and num != num_names[grid[r-1][c-1]-1]:
                    conflict = False
                problem += f"    (no-conflict {cell} {num})\n"

    problem += "  )\n\n"

    # Goal: all cells filled
    problem += "  (:goal (and\n"
    for pos in positions:
        problem += f"    (filled {pos})\n"
    problem += "  ))\n"
    problem += ")\n"

    with open(output_file, "w") as f:
        f.write(problem)