"""
generate_pddl_problem.py
Simple utility to programmatically build PDDL problem files for the 'grid' domain.
"""

import argparse
import random



def generate_keygrid_problem(n, filename):
    # Putting args in the local variables
    places = n * 3 + 1
    keys = n
    shapes = n
    locks = n
    seed = None

    density = 0.5

    # Apply seed if given
    if seed is not None:
        random.seed(seed)

    # Just to check
    print(";; Places:", places)
    print(";; Keys:", keys)
    print(";; Shapes:", shapes)
    print(";; Locks:", locks)
    print(";; Seed:", seed)


    # Starting generating a pddl file 

    # Step 2: Print the problem header
    with open(filename, 'w') as f:
        f.write(f"(define (problem grid-problem-{places}-{keys}-{locks}-{shapes})\n")
        f.write("  (:domain grid)\n")

        #Starting generating objects 
        f.write("  (:objects\n")

        # Places
        for i in range(1, places + 1):
            f.write(f"    place{i} - place\n")

        # Keys
        for i in range(1, keys + 1):
            f.write(f"    key{i} - key\n")

        # Shapes
        for i in range(1, shapes + 1):
            f.write(f"    shape{i} - shape\n")

        f.write("  )\n")  # end of :objects


        # Init section
        f.write("  (:init\n")

        # Connectivity: random undirected edges between places
        for i in range(1, places + 1):
            for j in range(i + 1, places + 1):
                if random.random() < density:  # 50% chance to connect, can make density an arg
                    f.write(f"    (conn place{i} place{j})\n")
                    f.write(f"    (conn place{j} place{i})\n")

        # Shapes: assign keys to random shapes
        for k in range(1, keys + 1):
            shape_id = random.randint(1, shapes)
            f.write(f"    (key-shape key{k} shape{shape_id})\n")

        # Locks: pick some places to be locked (not place1!)
        locked_places = random.sample(range(2, places + 1), min(locks, places - 1))
        for lp in locked_places:
            shape_id = random.randint(1, shapes)
            f.write(f"    (lock-shape place{lp} shape{shape_id})\n")
            f.write(f"    (locked place{lp})\n")

        # Place keys in random places
        for k in range(1, keys + 1):
            p = random.randint(1, places)
            f.write(f"    (at key{k} place{p})\n")

        # Robot start at place1
        f.write("    (at-robot place1)\n")

        # By default, place1 is open
        f.write("    (open place1)\n")

        # Arm empty at start
        f.write("    (arm-empty)\n")

        f.write("  )\n")  # end of :init

        # Goal section
        # Pick a random place (not place1) for the goal
        goal_place = random.randint(2, places)
        f.write("  (:goal\n")
        f.write("    (at-robot place" + str(goal_place) + ")\n")
        f.write("  )\n")

        f.write(")\n")  # close define

