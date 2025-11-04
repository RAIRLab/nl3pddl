#!/usr/bin/env python3
"""
Simple utility to build PDDL problem files for the 'sudoku' domain.
"""

import random

def generate_problem(n, output_file, seed=None):
    
    grid_size = n

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

    # Initialize all cells as empty and not-has-value for all numbers
    for r in range(grid_size):
        for c in range(grid_size):
            cell = f"r{r+1}c{c+1}"
            problem += f"    (empty {cell})\n"
            for num in num_names:
                problem += f"    (not-has-value {cell} {num})\n"

    # Override for pre-filled cells
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] != 0:
                cell = f"r{r+1}c{c+1}"
                num = num_names[grid[r][c]-1]
                problem += f"    (filled {cell})\n"
                problem += f"    (has-value {cell} {num})\n"
                problem += f"    (not (empty {cell}))\n"
                problem += f"    (not (not-has-value {cell} {num}))\n"

    # no-conflict relations
    for r in range(1, grid_size + 1):
        for c in range(1, grid_size + 1):
            cell = f"r{r}c{c}"
            for num in num_names:
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
