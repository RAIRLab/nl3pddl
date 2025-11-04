import argparse
import random

def count_inversions(tiles):
    arr = [t for t in tiles if t != "empty"]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def is_solvable(tiles, n):
    inversions = count_inversions(tiles)
    empty_index = tiles.index("empty")
    empty_row_from_bottom = n - (empty_index // n)

    if n % 2 == 1:
        # Odd grid: solvable if inversions even
        return inversions % 2 == 0
    else:
        # Even grid: solvable if (inversions + empty_row_from_bottom) is odd
        return (inversions + empty_row_from_bottom) % 2 == 1

def generate_sliding_puzzle_problem(n, filename, seed=42):
    random.seed(seed)

    size = n + 5 - 1
    tiles = [f"t{i}" for i in range(1, size + 1)]
    positions = [f"p{r}{c}" for r in range(1, n + 1) for c in range(1, n + 1)]

    # Create adjacency relations
    def neighbors(r, c):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr <= n and 1 <= nc <= n:
                yield (f"p{r}{c}", f"p{nr}{nc}")

    adjacencies = set()
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            for (p1, p2) in neighbors(r, c):
                adjacencies.add((p1, p2))

    # Generate a random *solvable* permutation
    while True:
        shuffled = [f"t{i}" for i in range(1, size + 1)] + ["empty"]
        random.shuffle(shuffled)
        if is_solvable(shuffled, n):
            break

    # Map tiles to positions
    tile_positions = []
    for tile, pos in zip(shuffled, positions):
        if tile != "empty":
            tile_positions.append((tile, pos))
    empty_pos = positions[shuffled.index("empty")]

    # Goal configuration
    goal_tile_positions = list(zip(tiles, positions[:size]))
    goal_empty = positions[-1]

    # Write PDDL
    with open(filename, "w") as f:
        f.write(f"(define (problem sliding-puzzle-{n}x{n})\n")
        f.write("  (:domain sliding-puzzle)\n\n")
        f.write("  (:objects\n")
        # Only write the tile type line if there are tiles. For 1x1, there are none.
        if tiles:
            f.write("    " + " ".join(tiles) + " - tile\n")
        f.write("    " + " ".join(positions) + " - position\n")
        f.write("  )\n\n")

        f.write("  (:init\n")
        for (t, p) in tile_positions:
            f.write(f"    (at {t} {p})\n")
        f.write(f"    (empty {empty_pos})\n\n")

        for (a, b) in sorted(adjacencies):
            f.write(f"    (adjacent {a} {b})\n")

        f.write("  )\n\n")

        f.write("  (:goal\n")
        f.write("    (and\n")
        for (t, p) in goal_tile_positions:
            f.write(f"      (at {t} {p})\n")
        f.write(f"      (empty {goal_empty})\n")
        f.write("    )\n")
        f.write("  )\n")
        f.write(")\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="grid size (e.g., 3 for 3x3)")
    parser.add_argument("output", type=str, help="output PDDL problem filename")
    parser.add_argument("--seed", type=int, default=42, help="random seed for reproducibility")
    args = parser.parse_args()

    generate_sliding_puzzle_problem(args.n, args.output, args.seed)
