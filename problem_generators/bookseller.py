#!/usr/bin/env python3
"""
generate_bookseller_problem.py

Generates random Bookseller problem instances in PDDL for the 'bookseller' domain.
"""

import argparse
import random

def generate_problem(n, output_file, seed=None):
    num_locations =  5
    num_books =  4
    num_drones = 2

    if seed is not None:
        random.seed(seed)

    # Names
    locations = [f"loc{i}" for i in range(1, num_locations + 1)]
    books     = [f"book{i}" for i in range(1, num_books + 1)]
    drones    = [f"drone{i}" for i in range(1, num_drones + 1)]
    # Assign random target locations for books
    book_targets = {book: random.choice(locations) for book in books}

    with open(output_file, 'w') as f:
        f.write(f"(define (problem bookseller-prob-{num_locations}loc-{num_books}bk-{num_drones}dr)\n")
        f.write("  (:domain bookseller)\n\n")
        # objects
        f.write("  (:objects\n")
        f.write("    " + " ".join(books)    + " - book\n")
        f.write("    " + " ".join(locations) + " - location\n")
        f.write("    " + " ".join(drones)    + " - drone\n")
        f.write("  )\n\n")
        # init
        f.write("  (:init\n")
        # book-at
        for b in books:
            loc = random.choice(locations)
            f.write(f"    (book-at {b} {loc})\n")
        f.write("\n")
        # drone-at and empty
        for d in drones:
            loc = random.choice(locations)
            f.write(f"    (drone-at {d} {loc})\n")
            f.write(f"    (empty {d})\n")
        f.write("\n")

        # path, there needs to be a cycle among all locations, with possible
        # additional connections, write to a dictionary to avoid duplicates
        path : dict[str, str] = {}
        for i in range(num_locations):
            path[locations[i]] = locations[(i + 1) % num_locations]
        # add additional random paths
        for _ in range(num_locations // 2):
            loc1, loc2 = random.sample(locations, 2)
            if loc2 not in path[loc1]:
                path[loc1] = loc2
        # write the paths
        for loc1, loc2 in path.items():
            f.write(f"    (path {loc1} {loc2})\n")
            f.write(f"    (path {loc2} {loc1})\n")

        f.write("  )\n\n")
        # goal: each book at its designated target location
        f.write("  (:goal (and\n")
        for b, target in book_targets.items():
            f.write(f"    (book-at {b} {target})\n")
        f.write("  ))\n")
        f.write(")\n")

    print(f"Generated PDDL problem: {output_file}")
