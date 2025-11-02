import argparse
import random

def generate_solvable_keygrid(n, filename):

    locks = n
    keys = n
    shapes = n

    # Total number of places: n locked segments + n extra open places + start
    places = n * 2 + 1  

    # Fixed seed for reproducibility
    seed = 42
    random.seed(seed)

    with open(filename, 'w') as f:

        # Header comment
        f.write(f";; Solvable KeyGrid: places={places}, keys={keys}, locks={locks}, shapes={shapes}, seed={seed}\n")

        # Problem header
        f.write(f"(define (problem grid-problem-{places}-{keys}-{locks}-{shapes})\n")
        f.write(" (:domain grid)\n")

        # Objects
        f.write(" (:objects\n")
        for i in range(1, places + 1):
            f.write(f"  place{i} - place\n")
        for i in range(1, keys + 1):
            f.write(f"  key{i} - key\n")
        for i in range(1, shapes + 1):
            f.write(f"  shape{i} - shape\n")
        f.write(" )\n")

    
        # Init
        f.write(" (:init\n")

        # Linear chain topology
        for i in range(1, places):
            f.write(f"  (conn place{i} place{i+1})\n")
            f.write(f"  (conn place{i+1} place{i})\n")

        # Locks and keys
        # lock is placed at place(i+1)
        for i in range(1, locks + 1):
            f.write(f"  (key-shape key{i} shape{i})\n")
            f.write(f"  (lock-shape place{i+1} shape{i})\n")
            f.write(f"  (locked place{i+1})\n")

        # Place key i at place i (so robot always finds correct key before its lock)
        for i in range(1, keys + 1):
            f.write(f"  (at key{i} place{i})\n")

        f.write("  (at-robot place1)\n")
        f.write("  (open place1)\n")
        f.write("  (arm-empty)\n")

    
        # All places AFTER the last lock must be open or the robot can't move into them.
        last_locked_place = locks + 1
        for p in range(last_locked_place + 1, places + 1):
            f.write(f"  (open place{p})\n")

        f.write(" )\n")  # end init

        # Goal – reach the *last* place
        f.write(" (:goal\n")
        f.write(f"  (at-robot place{places})\n")
        f.write(" )\n")

        f.write(")\n")  # end problem


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a solvable PDDL KeyGrid problem.")
    parser.add_argument("n", type=int, help="number of locks/keys/shapes")
    parser.add_argument("output", type=str, help="output filename")
    args = parser.parse_args()

    generate_solvable_keygrid(args.n, "../../data/domains/grid/problem_generated.pddl")
