"""
hiking.py
Generates guaranteed-solvable PDDL problems for the 'hiking' domain.
"""

import argparse
import random

def generate_hiking_problem(n, filename, seed=None, density=0.4):
    locations = n * 2 + 1
    hills = n
    waters = n

    if seed is not None:
        random.seed(seed)

    # Sanity check
    if locations < 3:
        raise ValueError("There must be at least 3 locations (start, goal, and one middle).")

    loc_ids = list(range(1, locations + 1))
    start = loc_ids[0]
    goal = loc_ids[-1]

    # Ensure a solvable backbone path
    path = [start]
    remaining = loc_ids[1:-1]
    random.shuffle(remaining)
    path += remaining + [goal]

    # Create edges forming a guaranteed path
    edges = set()
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        edges.add((a, b))
        edges.add((b, a))

    # Add random extra connections for variety
    for i in loc_ids:
        for j in loc_ids:
            if i < j and (i, j) not in edges and random.random() < density:
                edges.add((i, j))
                edges.add((j, i))

    # Pick hill and water locations (not on the backbone path)
    safe_locs = set(path)  # do not make these water
    possible = [loc for loc in loc_ids[1:-1] if loc not in safe_locs]
    random.shuffle(possible)

    hill_locs = random.sample(loc_ids[1:-1], min(hills, len(loc_ids)-2))
    water_candidates = [l for l in loc_ids[1:-1] if l not in hill_locs and l not in path]
    water_locs = random.sample(water_candidates, min(waters, len(water_candidates)))

    # Write PDDL file
    with open(filename, 'w') as f:
        f.write(f";; Hiking problem generator (solvable version)\n")
        f.write(f";; Locations: {locations}, Hills: {hills}, Waters: {waters}, Seed: {seed}\n\n")

        f.write(f"(define (problem hiking-problem-{locations}-{hills}-{waters})\n")
        f.write("  (:domain hiking)\n\n")

        # Objects
        f.write("  (:objects\n")
        for i in loc_ids:
            f.write(f"    loc{i} - loc\n")
        f.write("  )\n\n")

        # Init
        f.write("  (:init\n")
        f.write(f"    (at loc{start})\n")

        # Write adjacency
        for (a, b) in sorted(edges):
            f.write(f"    (adjacent loc{a} loc{b})\n")

        # Hills
        for h in sorted(hill_locs):
            f.write(f"    (isHill loc{h})\n")

        # Water (avoid path nodes)
        for w in sorted(water_locs):
            f.write(f"    (isWater loc{w})\n")

        # Goal
        f.write(f"    (isGoal loc{goal})\n")
        f.write("  )\n\n")

        # Goal section
        f.write(f"  (:goal (at loc{goal}))\n")
        f.write(")\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solvable Hiking domain problem generator")
    parser.add_argument("n", type=int, help="Number of terrain features (controls size)")
    parser.add_argument("filename", type=str, help="Output PDDL filename")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--density", type=float, default=0.4, help="Extra edge density")

    args = parser.parse_args()
    generate_hiking_problem(args.n, args.filename, seed=args.seed, density=args.density)
