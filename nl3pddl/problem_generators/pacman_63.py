"""
Generates a 2D grid-based Pacman problem for the 'pacman-63' domain.
"""

import random

def generate_pacman_ai_problem(n, output_file, seed=None):

    num_nodes = n + 3           # grid dimension
    num_food = n + 1
    num_ghosts = n + 2          # unsafe nodes

    if seed is not None:
        random.seed(seed)

    # Create all nodes for the matrix
    nodes = [f"n{i}_{j}" for i in range(num_nodes) for j in range(num_nodes)]

    # Randomly select start and food nodes
    start_node = random.choice(nodes)
    food_nodes = random.sample(nodes, min(num_food, len(nodes)))

    # Ensure start and food nodes are safe
    must_be_safe = set([start_node] + food_nodes)

    # Randomly assign unsafe (ghost) nodes from remaining ones
    candidates = [node for node in nodes if node not in must_be_safe]
    unsafe_nodes = set(random.sample(candidates, min(num_ghosts, len(candidates))))
    safe_nodes = [n for n in nodes if n not in unsafe_nodes]

    # Create 4-directional connectivity (up, down, left, right)
    connections = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            node = f"n{i}_{j}"
            # Down
            if i + 1 < num_nodes:
                connections.append((node, f"n{i+1}_{j}"))
                connections.append((f"n{i+1}_{j}", node))
            # Right
            if j + 1 < num_nodes:
                connections.append((node, f"n{i}_{j+1}"))
                connections.append((f"n{i}_{j+1}", node))

    # Build the PDDL problem text
    problem = f"(define (problem pacman-63)\n"
    problem += "    (:domain pacman-63)\n"
    problem += "    (:objects\n"
    problem += "        " + " ".join(nodes) + " - node\n"
    problem += "    )\n\n"

    # Initial state
    problem += "    (:init\n"

    # Pacman's position
    for node in nodes:
        if node == start_node:
            problem += f"        (at {node})\n"
        else:
            problem += f"        (not_at {node})\n"

    # Food distribution
    for node in nodes:
        if node in food_nodes:
            problem += f"        (has_food {node})\n"
        else:
            problem += f"        (no_food {node})\n"

    # Safety assignment
    for node in safe_nodes:
        problem += f"        (is_safe {node})\n"

    # Graph connections
    for (a, b) in connections:
        problem += f"        (connected {a} {b})\n"

    problem += "    )\n\n"

    # Goal: all food eaten
    problem += "    (:goal (and\n"
    for fn in food_nodes:
        problem += f"        (no_food {fn})\n"
    problem += "    ))\n"
    problem += ")\n"

    # Write to file
    with open(output_file, "w") as f:
        f.write(problem)