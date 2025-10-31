"""
Simple utility to build PDDL problem files for the 'pacman-72' domain.
"""

import random

def generate_pacman_problem(n, output_file, seed=None):
    grid_size = n + 3
    num_food = n + 2 

    if seed is not None:
        random.seed(seed)

    # Generate position names
    positions = [f"p{x}{y}" for x in range(grid_size) for y in range(grid_size)]

    # Randomly choose start position and food positions
    start_pos = random.choice(positions)
    food_positions = random.sample(positions, min(num_food, len(positions)))

    # Build connections (grid adjacency)
    neighbors = []
    for x in range(grid_size):
        for y in range(grid_size):
            current = f"p{x}{y}"
            if x + 1 < grid_size:
                neighbors.append((current, f"p{x+1}{y}"))
                neighbors.append((f"p{x+1}{y}", current))
            if y + 1 < grid_size:
                neighbors.append((current, f"p{x}{y+1}"))
                neighbors.append((f"p{x}{y+1}", current))

    # Start building PDDL content
    problem = f"(define (problem pacman-72-prob-{n})\n"
    problem += "    (:domain pacman-72)\n"
    problem += "    (:objects\n"
    problem += "        " + " ".join(positions) + " - position\n"
    problem += "    )\n\n"

    # Initial state without negated predicates
    problem += "    (:init\n"
    problem += f"        (at {start_pos})\n"
    for pos in positions:
        if pos in food_positions:
            problem += f"        (hasFood {pos})\n"
    for (a, b) in neighbors:
        problem += f"        (connected {a} {b})\n"
    problem += "    )\n\n"

    # Goal: all food picked up
    problem += "    (:goal (and\n"
    for f in food_positions:
        problem += f"        (noFood {f})\n"
    problem += "    ))\n"
    problem += ")\n"

    # Write to file
    with open(output_file, "w") as f:
        f.write(problem)