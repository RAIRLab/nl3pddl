#!/usr/bin/env python3
"""
generate_blocks_problem.py

Generates random Blocksworld problem instances in PDDL for the 'blocks' domain.
"""

import argparse
import random
import textwrap

def generate_problem(n, output_file, seed=None):

    num_blocks = 2 * n

    if seed is not None:
        random.seed(seed)

    # Block names
    blocks = [f"b{i}" for i in range(1, num_blocks + 1)]

    # Helper: create random stacks (list of lists)
    def random_stacks():
        # choose number of stacks between 1 and num_blocks
        k = random.randint(1, num_blocks)
        perm = blocks[:]
        random.shuffle(perm)
        # partition perm into k roughly equal stacks
        sizes = [num_blocks // k + (1 if i < (num_blocks % k) else 0) for i in range(k)]
        stacks, idx = [], 0
        for size in sizes:
            stacks.append(perm[idx: idx + size])
            idx += size
        return stacks

    init_stacks = random_stacks()
    goal_stacks = random_stacks()

    # Begin writing PDDL
    with open(output_file, 'w') as f:
        f.write(f"(define (problem blocks-prob-{n}"
                + (f"-seed{seed}" if seed is not None else "") + ")\n")
        f.write("  (:domain blocks)\n\n")

        # Objects
        f.write("  (:objects\n")
        for b in blocks:
            f.write(f"    {b} - block\n")
        f.write("  )\n\n")

        # Initial state
        f.write("  (:init\n")
        # Place blocks on table or on other blocks
        for stack in init_stacks:
            if len(stack) == 1:
                f.write(f"    (ontable {stack[0]})\n")
            else:
                f.write(f"    (ontable {stack[0]})\n")
                for upper, lower in zip(stack[1:], stack):
                    f.write(f"    (on {upper} {lower})\n")
        # Clear predicates for tops of each stack
        for stack in init_stacks:
            top = stack[-1]
            f.write(f"    (clear {top})\n")
        # Hand is empty
        f.write("    (handempty)\n")
        f.write("  )\n\n")

        # Goal state
        f.write("  (:goal (and\n")
        for stack in goal_stacks:
            if len(stack) == 1:
                f.write(f"    (ontable {stack[0]})\n")
            else:
                f.write(f"    (ontable {stack[0]})\n")
                for upper, lower in zip(stack[1:], stack):
                    f.write(f"    (on {upper} {lower})\n")
        f.write("  ))\n")
        f.write(")\n")

    print(f"Generated PDDL problem: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate random Blocksworld PDDL problem instances."
    )
    parser.add_argument(
        "num_blocks", type=int, help="Number of blocks to include."
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output PDDL filename (default: blocks-prob-<num_blocks>.pddl)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Optional random seed for reproducibility."
    )
    args = parser.parse_args()

    out_file = args.output or f"blocks-prob-{args.num_blocks}.pddl"
    generate_problem(args.num_blocks, out_file, args.seed)