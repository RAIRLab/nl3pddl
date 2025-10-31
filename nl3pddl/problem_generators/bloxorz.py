"""
Simple utility to build PDDL problem files for the 'bloxorz' domain.
"""

import random

def generate_bloxorz_problem(grid_size, path_length, output_file, seed=None):
    
    width, height = grid_size
    if seed is not None:
        random.seed(seed)

    # Create tiles
    tiles = [f"t{x}_{y}" for x in range(width) for y in range(height)]

    # Generate a solvable path for the block
    def random_walk(start, length):
        path = [start]
        for _ in range(length - 1):
            x, y = map(int, path[-1][1:].split("_"))
            neighbors = []
            if y > 0: neighbors.append(f"t{x}_{y-1}")
            if y < height - 1: neighbors.append(f"t{x}_{y+1}")
            if x > 0: neighbors.append(f"t{x-1}_{y}")
            if x < width - 1: neighbors.append(f"t{x+1}_{y}")
            neighbors = [n for n in neighbors if n not in path]
            if not neighbors:
                break
            path.append(random.choice(neighbors))
        return path

    start_tile = random.choice(tiles)
    path = random_walk(start_tile, path_length)
    goal_tile = path[-1]

    # Build adjacency facts
    adjacency = []
    for tile in tiles:
        x, y = map(int, tile[1:].split("_"))
        if y > 0: adjacency.append((tile, f"t{x}_{y-1}", "north"))
        if y < height - 1: adjacency.append((tile, f"t{x}_{y+1}", "south"))
        if x < width - 1: adjacency.append((tile, f"t{x+1}_{y}", "east"))
        if x > 0: adjacency.append((tile, f"t{x-1}_{y}", "west"))

    # Build the PDDL content
    problem = f"(define (problem bloxorz-prob-{width}x{height})\n"
    problem += "    (:domain bloxorz)\n"
    problem += "    (:objects\n"
    problem += "        " + " ".join(tiles) + " - tile\n"
    problem += "        b1 - block\n"
    problem += "    )\n\n"

    # Initial state
    problem += "    (:init\n"
    problem += f"        (on b1 {start_tile})\n"
    for t1, t2, dir in adjacency:
        problem += f"        (adjacent-{dir} {t1} {t2})\n"
    problem += f"        (-tile {goal_tile})\n"
    problem += "    )\n\n"

    # Goal
    problem += f"    (:goal (on b1 {goal_tile}))\n"
    problem += ")\n"

    with open(output_file, "w") as f:
        f.write(problem)