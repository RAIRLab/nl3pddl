"""
Simple utility to build PDDL problem files for the 'pacman-72' domain.
"""

import random

def generate_pacman_problem(n, output_file, seed=None):
    
    grid_size = n + 3
    num_food = n + 2 

    if seed is not None:
        random.seed(seed)

    positions = [f"p{x}{y}" for x in range(grid_size) for y in range(grid_size)]

    # Randomly choose a start position and food positions
    start_pos = random.choice(positions)
    food_positions = random.sample(positions, min(num_food, len(positions)))

    # Build connected grid (grid adjacency)
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

    # PDDL problem
    problem = f"(define (problem pacman-72)\n"
    problem += "    (:domain pacman-72)\n"
    problem += "    (:objects\n"
    problem += "        " + " ".join(positions) + " - position\n"
    problem += "    )\n\n"

    # Initial states
    problem += "    (:init\n"

    # Initialize at/not_at predicates
    for pos in positions:
        if pos == start_pos:
            problem += f"        (at {pos})\n"
            problem += f"        (not (not_at {pos}))\n"
        else:
            problem += f"        (not_at {pos})\n"
            problem += f"        (not (at {pos}))\n"

    # Initialize hasFood/noFood predicates
    for pos in positions:
        if pos in food_positions:
            problem += f"        (hasFood {pos})\n"
            problem += f"        (not (noFood {pos}))\n"
        else:
            problem += f"        (noFood {pos})\n"
            problem += f"        (not (hasFood {pos}))\n"

    # Connections
    for (a, b) in neighbors:
        problem += f"        (connected {a} {b})\n"

    problem += "    )\n\n"

    # The goal: all food picked up
    problem += "    (:goal (and\n"
    for f in food_positions:
        problem += f"        (noFood {f})\n"
    problem += "    ))\n"
    problem += ")\n"

    with open(output_file, "w") as f:
        f.write(problem)