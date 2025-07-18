import argparse
import random

def generate_problem(n, output_file, seed=None):
    num_floors = n + 2
    num_passengers = n + 2

    if seed is not None:
        random.seed(seed)

    # Create names
    floors = [f"f{i}" for i in range(1, num_floors + 1)]
    passengers = [f"p{i}" for i in range(1, num_passengers + 1)]

    # Assign random origins and destinations (distinct)
    origin = {}
    destin = {}
    for p in passengers:
        o = random.choice(floors)
        d = random.choice(floors)
        while d == o:
            d = random.choice(floors)
        origin[p] = o
        destin[p] = d

    # Choose initial lift position
    start_floor = random.choice(floors)

    with open(output_file, 'w') as f:
        f.write(f"(define (problem miconic-prob-{num_floors}f-{num_passengers}p")
        if seed is not None:
            f.write(f"-seed{seed}")
        f.write(")\n")
        f.write("  (:domain miconic)\n\n")

        # Objects
        f.write("  (:objects\n")
        f.write("    " + " ".join(passengers) + " - passenger\n")
        f.write("    " + " ".join(floors) + " - floor\n")
        f.write("  )\n\n")

        # Initial state
        f.write("  (:init\n")
        # origin and destin predicates
        for p in passengers:
            f.write(f"    (origin {p} {origin[p]})\n")
            f.write(f"    (destin {p} {destin[p]})\n")
            f.write(f"    (not-boarded {p})\n")
            f.write(f"    (not-served {p})\n")
        # above relations (i<j)
        for i in range(num_floors):
            for j in range(i+1, num_floors):
                f.write(f"    (above {floors[i]} {floors[j]})\n")
        # lift position
        f.write(f"    (lift-at {start_floor})\n")
        # also ensure no one is boarded and no one served removed (errors in domain),
        # but boarded and served initially false
        f.write("  )\n\n")

        # Goal: everyone served
        f.write("  (:goal (and\n")
        for p in passengers:
            f.write(f"    (served {p})\n")
        f.write("  ))\n")
        f.write(")\n")

    print(f"Generated PDDL problem: {output_file}")
