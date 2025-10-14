"""
    Simple utility to build PDDL problem files for the 'pacman-63' domain.
"""

import random

def generate_pacman_ai_problem(n, output_file, seed=None):
    
    num_nodes = n + 3
    num_food = n + 1
    num_ghosts = n
    
    if (seed is not None):
        random.seed(seed)

    # Create nodes
    nodes = [f"n{i}" for i in range(num_nodes)]

    # Randomly assign start, food, and ghost locations
    start_node = random.choice(nodes)
    food_nodes = random.sample(nodes, min(num_food, len(nodes)))
    ghost_nodes = random.sample(
        [n for n in nodes if n not in food_nodes and n != start_node],
        min(num_ghosts, len(nodes) - len(food_nodes) - 1)
    )

    # Build full connectivity (undirected graph)
    connections = []
    for i in range(num_nodes - 1):
        connections.append((nodes[i], nodes[i + 1]))
        connections.append((nodes[i + 1], nodes[i]))

    # Build the PDDL content
    problem = f"(define (problem pacman-63-prob-{n})\n"
    problem += "    (:domain pacman_ai)\n"
    problem += "    (:objects\n"
    problem += "        " + " ".join(nodes) + " - node\n"
    problem += "    )\n\n"

    # Initial state
    problem += "    (:init\n"
    problem += f"        (at {start_node})\n"
    for fn in food_nodes:
        problem += f"        (has_food {fn})\n"
    for gn in ghost_nodes:
        problem += f"        (is_opponent_ghost {gn})\n"
    for (a, b) in connections:
        problem += f"        (connected {a} {b})\n"
    problem += "    )\n\n"

    # Goal: all food eaten (no has_food anywhere)
    problem += "    (:goal (and\n"
    for fn in food_nodes:
        problem += f"        (not (has_food {fn}))\n"
    problem += "    ))\n"
    problem += ")\n"

    with open(output_file, "w") as f:
        f.write(problem)