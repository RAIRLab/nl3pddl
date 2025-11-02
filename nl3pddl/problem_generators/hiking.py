"""
hiking.py
Generates guaranteed-solvable PDDL problems for the 'hiking' domain.
"""

import argparse
import random
from collections import deque


def bfs_path(adj, start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for nbr in adj[node]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append(path + [nbr])
    return None

#test
def generate_hiking_problem(n, filename, density=0.5, water_ratio=0.5, seed=None):
    if seed is not None:
        random.seed(seed)

    if n < 1:
        n = 1

    locations = n * 2 + 1
    
    adj = {i: set() for i in range(1, locations + 1)}

    # Build spanning tree
    unvisited = list(range(2, locations + 1))
    connected = [1]
    while unvisited:
        from_loc = random.choice(connected)
        to_loc = random.choice(unvisited)
        adj[from_loc].add(to_loc)
        adj[to_loc].add(from_loc)
        connected.append(to_loc)
        unvisited.remove(to_loc)

    # Add extra edges
    for i in range(1, locations + 1):
        for j in range(i + 1, locations + 1):
            if random.random() < density:
                adj[i].add(j)
                adj[j].add(i)

    # Find a guaranteed path from start to goal ---
    dry_path = bfs_path(adj, 1, locations)

    dry_set = set(dry_path)

    # Randomly assign dry/wet locations
    all_nodes = set(range(1, locations + 1))
    wet_candidates = list(all_nodes - dry_set)
    num_water = int(len(wet_candidates) * water_ratio)
    wet_locs = set(random.sample(wet_candidates, num_water))
    dry_locs = all_nodes - wet_locs

    # Assign terrain (hill/flat)
    inner_locs = list(range(2, locations))  # exclude start and goal
    random.shuffle(inner_locs)
    num_hills = min(n, len(inner_locs))
    hill_locs = set(inner_locs[:num_hills])
    flat_locs = set(inner_locs[num_hills:])

    # Write the problem file
    with open(filename, "w") as f:
        f.write(f";; Solvable Hiking problem with water\n")
        f.write(f";; Locations: {locations}, Hills: {n}, Water: {len(wet_locs)}\n\n")

        f.write(f"(define (problem hiking-problem-{locations})\n")
        f.write("  (:domain hiking)\n\n")

        f.write("  (:objects\n")
        for i in loc_ids:
            f.write(f"    loc{i} - loc\n")
        f.write("  )\n\n")

        # Init
        f.write("  (:init\n")
        f.write("    (at loc1)\n")

        # Adjacencies
        for i in range(1, locations + 1):
            for j in sorted(adj[i]):
                f.write(f"    (adjacent loc{i} loc{j})\n")

        # Terrain
        for h in hill_locs:
            f.write(f"    (isHill loc{h})\n")
        for fl in flat_locs:
            f.write(f"    (isFlat loc{fl})\n")

        # So the final location always has a terrain
        if locations not in hill_locs and locations not in flat_locs:
            f.write(f"    (isFlat loc{locations})\n")

        # Dryness
        for d in sorted(dry_locs):
            f.write(f"    (isDry loc{d})\n")

        f.write("  )\n\n")
        f.write(f"  (:goal (at loc{locations}))\n")
        f.write(")\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a solvable hiking PDDL problem with water.")
    parser.add_argument("n", type=int, default=3, help="Number of hills (problem size).")
    parser.add_argument("output", type=str, default="hiking_problem_with_water.pddl", help="Output filename.")
    parser.add_argument("--density", type=float, default=0.5, help="Extra adjacency density (0–1).")
    parser.add_argument("--water", type=float, default=0.3, help="Fraction of locations to make wet (0–1).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    args = parser.parse_args()

    generate_hiking_problem(args.n, args.output, args.density, args.water, args.seed)
