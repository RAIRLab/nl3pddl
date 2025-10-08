"""
Simple utility to programmatically build PDDL problem files for the 'hiking' domain.
"""

import argparse
import random

def generate_hiking_problem(n, filename):
    locations = n * 2 + 1
    hills = n
    waters = n
    seed = None
    density = 0.5

    if seed is not None:
        random.seed(seed)

    # Sanity check
    if locations < 3:
        raise ValueError("There must be at least 3 locations (start, goal, and one middle).")

    with open(filename, 'w') as f:
        f.write(f";; Hiking problem generator\n")
        f.write(f";; Locations: {locations}, Hills: {hills}, Waters: {waters}, Seed: {seed}\n\n")

        # Start generating the PDDL problem
        f.write(f"(define (problem hiking-problem-{locations}-{hills}-{waters})\n")
        f.write("  (:domain hiking)\n\n")

        # Objects
        f.write("  (:objects\n")
        for i in range(1, locations + 1):
            f.write(f"    loc{i} - loc\n")
        f.write("  )\n\n")

        # Init section
        f.write("  (:init\n")

        # Start location
        f.write("    (at loc1)\n")

        # Generate random adjacency (undirected)
        for i in range(1, locations + 1):
            for j in range(i + 1, locations + 1):
                if random.random() < density:
                    f.write(f"    (adjacent loc{i} loc{j})\n")
                    f.write(f"    (adjacent loc{j} loc{i})\n")

        # Assign hills and waters
        all_locs = list(range(2, locations))  # exclude loc1 (start) and last (goal)
        random.shuffle(all_locs)

        hill_locs = all_locs[:min(hills, len(all_locs))]
        water_locs = all_locs[min(hills, len(all_locs)):min(hills + waters, len(all_locs))]

        for h in hill_locs:
            f.write(f"    (isHill loc{h})\n")

        for w in water_locs:
            f.write(f"    (isWater loc{w})\n")

        # Mark goal location
        f.write(f"    (isGoal loc{locations})\n")

        f.write("  )\n\n")  # end of :init

        # Goal section
        f.write("  (:goal (at loc" + str(locations) + "))\n\n")

        f.write(")")  # end of problem definition
