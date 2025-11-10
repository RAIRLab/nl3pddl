"""
Utility to build PDDL problem files for the 'sudoku' domain.
"""

import random

def generate_sudoku_problem(output_file, seed=None):
    grid_size = 4  # 4x4 Sudoku example

    if seed is not None:
        random.seed(seed)

    digits = [1, 2, 3, 4]
    num_names = ["one", "two", "three", "four"]
    rows = [f"r{i}" for i in range(1, grid_size + 1)]
    cols = [f"c{i}" for i in range(1, grid_size + 1)]
    boxes = [f"b{i}" for i in range(1, grid_size + 1)]
    positions = [f"p{r}{c}" for r in range(1, grid_size + 1) for c in range(1, grid_size + 1)]

    # Create an empty grid
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Randomly assign one of each number to unique cells
    used_positions = random.sample(positions, len(digits))
    for pos, digit in zip(used_positions, digits):
        r = int(pos[1]) - 1
        c = int(pos[2]) - 1
        grid[r][c] = digit

    # Start writing PDDL problem
    problem = "(define (problem sudoku)\n"
    problem += "  (:domain sudoku)\n\n"

    # Objects
    problem += "  (:objects\n"
    problem += "    " + " ".join(positions) + " - pos\n"
    problem += "    " + " ".join(rows) + " - row\n"
    problem += "    " + " ".join(cols) + " - col\n"
    problem += "    " + " ".join(boxes) + " - box\n"
    problem += "    " + " ".join(num_names) + " - number\n"
    problem += "  )\n\n"

    # Init section
    problem += "  (:init\n"

    # Position data
    for r in range(grid_size):
        for c in range(grid_size):
            pos = f"p{r+1}{c+1}"
            row = f"r{r+1}"
            col = f"c{c+1}"
            box = f"b{(r // 2) * 2 + (c // 2) + 1}"
            problem += f"    (posdata {pos} {row} {col} {box})\n"

    # Mark all positions empty initially
    for pos in positions:
        problem += f"    (empty {pos})\n"

    # Pre-filled cells
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] != 0:
                pos = f"p{r+1}{c+1}"
                num = num_names[grid[r][c] - 1]
                box = f"b{(r // 2) * 2 + (c // 2) + 1}"

                # Mark position as filled (no need for not-empty)
                problem += f"    (filled {pos})\n"

                # not-in-row for all other rows
                for other_r in rows:
                    if other_r != f"r{r+1}":
                        problem += f"    (not-in-row {num} {other_r})\n"

                # not-in-col for all other columns
                for other_c in cols:
                    if other_c != f"c{c+1}":
                        problem += f"    (not-in-col {num} {other_c})\n"

                # not-in-box for all other boxes
                for other_b in boxes:
                    if other_b != box:
                        problem += f"    (not-in-box {num} {other_b})\n"

    problem += "  )\n\n"

    # Goal: all positions filled
    problem += "  (:goal (and\n"
    for pos in positions:
        problem += f"    (filled {pos})\n"
    problem += "  ))\n"
    problem += ")\n"

    # Write to file
    with open(output_file, "w") as f:
        f.write(problem)
