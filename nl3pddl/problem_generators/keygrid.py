import argparse
import random

def generate_keygrid_problem(n, filename):
    
    locks = n           # Number of locked doors (place2 to place_{n+1})
    keys = n            # Number of unique keys (key1 to key_n)
    shapes = n          # Number of unique shapes (shape1 to shape_n)
    
    places = n * 2 + 1 
    
    # Use a fixed seed for reproducibility
    seed = 42
    random.seed(seed)

    # --- Information Header ---
    print(f";; Generating solvable problem with {places} places, {keys} keys, {locks} locks, {shapes} shapes, seed={seed}")
    
    # NOTE: The bounds check in the original generator is confusing and not needed if the parameters are derived correctly.
    # keys = min(keys, locks) 
    # locks = min(locks, places - 1)
    # shapes = max(shapes, locks)

    with open(filename, 'w') as f:
        # Header
        f.write(f"(define (problem keygrid-problem-{places}-{keys}-{locks}-{shapes})\n")
        f.write("  (:domain keygrid)\n")

        # Objects
        f.write("  (:objects\n")
        for i in range(1, places + 1):
            f.write(f"    place{i} - place\n")
        for i in range(1, keys + 1):
            f.write(f"    key{i} - key\n")
        # Ensure we define shapes up to the highest shape_id used (which is 'shapes')
        for i in range(1, shapes + 1): 
            f.write(f"    shape{i} - shape\n")
        f.write("  )\n")

        # Init
        f.write("  (:init\n")

        # Connect places in a linear chain
        for i in range(1, places):
            f.write(f"    (conn place{i} place{i+1})\n")
            f.write(f"    (conn place{i+1} place{i})\n")

        # Assign locks and keys (Locks are on place2 to place_{n+1})
        for i in range(1, locks + 1):
            shape_id = i
            # Key definition
            f.write(f"    (key-shape key{i} shape{shape_id})\n")
            # Lock definition (place_{i+1} is the door)
            f.write(f"    (lock-shape place{i+1} shape{shape_id})\n")
            f.write(f"    (locked place{i+1})\n")

        # Place each key before its lock (key_i at place_i)
        # This is the essential part for solvability using the pickup-and-loose chain
        for i in range(1, keys + 1):
            f.write(f"    (at key{i} place{i})\n")

        # Robot initial state
        f.write("    (at-robot place1)\n")
        f.write("    (open place1)\n")
        f.write("    (arm-empty)\n")

        f.write("  )\n")  # end init

        # Goal
        f.write("  (:goal\n")
        f.write(f"    (at-robot place{places})\n")
        f.write("  )\n")

        f.write(")\n")  # end define

    print(f"Generated solvable problem: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a solvable PDDL KeyGrid problem.")
    parser.add_argument("n", type=int, help="number of locks/keys/shapes (complexity, e.g., 10 creates the example problem)")
    parser.add_argument("output", type=str, help="output filename (e.g., problem.pddl)")
    args = parser.parse_args()
    
    if args.n < 1:
         print("Error: 'n' must be a positive integer (number of locks).")
    else:
        generate_solvable_keygrid(args.n, args.output)