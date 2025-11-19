
#!/usr/bin/env python3
"""
Randomly generate a maze of size n x m with k walkable tiles, plus one B (start) and one G (goal),
printed in the same text format as your earlier example.

Legend:
  'X' - walkable tile
  'B' - start tile (also walkable)
  'G' - goal tile (also walkable)
   ' ' - empty (no tile)

Connectivity:
  The set of tiles is guaranteed to be 4-neighbor connected so B and G are reachable.

Strategy:
  We grow a connected set of tiles using a randomized frontier expansion (Prim-like growth),
  until we have (k + 2) tiles. We then place 'B' and 'G' on two distinct tiles (by default
  far apart along a random spanning-tree path for good separation).

Usage:
  python gen_random_maze.py --rows 6 --cols 10 --k 20 --seed 42 --semicolon
  (omit --semicolon to avoid leading '; ' on each line)

  You can also import and call generate_maze(n, m, k, seed=None, semicolon=False) to get a string.
"""

from __future__ import annotations
import argparse
import random
from collections import deque
from typing import List, Set, Tuple, Optional

Coord = Tuple[int, int]  # (row, col), 0-based internally


def neighbors(r: int, c: int, n: int, m: int):
    if r > 0: yield (r - 1, c)
    if r + 1 < n: yield (r + 1, c)
    if c > 0: yield (r, c - 1)
    if c + 1 < m: yield (r, c + 1)


def grow_connected_cells(n: int, m: int, target: int, rng: random.Random) -> Set[Coord]:
    """
    Grow a connected set of 'target' distinct cells within an n x m grid using
    randomized frontier expansion (like Prim's algorithm). Always succeeds if
    target <= n*m and target >= 1.
    """
    # Start from a random cell
    start = (rng.randrange(n), rng.randrange(m))
    selected: Set[Coord] = {start}
    frontier: List[Coord] = []

    # Initialize frontier with neighbors of start
    for nb in neighbors(*start, n, m):
        if nb not in selected:
            frontier.append(nb)

    while len(selected) < target:
        if not frontier:
            # If we ran out of frontier (can happen in degenerate cases), pick a random
            # neighbor of the current set that isn't selected yet — rebuild frontier.
            # This ensures progress unless target > n*m (which we forbid).
            all_frontier = set()
            for r, c in list(selected):
                for nb in neighbors(r, c, n, m):
                    if nb not in selected:
                        all_frontier.add(nb)
            frontier = list(all_frontier)
            if not frontier:
                # Should not happen if target <= n*m, but guard anyway
                raise RuntimeError("Failed to expand frontier; grid exhausted unexpectedly.")

        # Pick a random frontier cell to add
        idx = rng.randrange(len(frontier))
        cell = frontier.pop(idx)
        if cell in selected:
            continue
        selected.add(cell)

        # Add its neighbors to frontier
        for nb in neighbors(*cell, n, m):
            if nb not in selected:
                frontier.append(nb)

    return selected


def far_apart_endpoints(cells: Set[Coord], n: int, m: int, rng: random.Random) -> Tuple[Coord, Coord]:
    """
    Choose two tiles far apart (by BFS in the induced subgraph of 'cells') to use as B (start) and G (goal).
    Returns (b, g).
    """
    # Build adjacency within 'cells'
    def bfs(src: Coord) -> Tuple[Coord, dict]:
        q = deque([src])
        dist = {src: 0}
        parent = {src: None}
        while q:
            u = q.popleft()
            for v in neighbors(*u, n, m):
                if v in cells and v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
        # Farthest node from src
        far = max(dist, key=lambda x: dist[x])
        return far, parent

    # Pick an arbitrary start
    any_cell = next(iter(cells))
    a, _ = bfs(any_cell)           # farthest from arbitrary
    b, parent = bfs(a)             # farthest from a (approx diameter end)

    # a and b are far apart; use them for B and G but randomize assignment
    if rng.random() < 0.5:
        return a, b
    else:
        return b, a


def generate_maze(n: int, m: int, k: int, seed: Optional[int] = None, semicolon: bool = False) -> str:
    """
    Generate an n x m maze text with exactly k 'X' tiles plus one 'B' and one 'G'.

    Returns the maze as a string with n lines of length up to m.
    Since it's a full rectangular grid, lines are exactly length m.
    If semicolon=True, each line is prefixed with '; '.

    Constraints:
      - n >= 1, m >= 1
      - k >= 0
      - k + 2 <= n * m  (room for B and G)
    """
    if n < 1 or m < 1:
        raise ValueError("n and m must be >= 1.")
    if k < 0:
        raise ValueError("k must be >= 0.")
    if k + 2 > n * m:
        raise ValueError("k + 2 must be <= n * m (need space for B and G).")

    rng = random.Random(seed)
    total_tiles = k + 2
    # Grow a connected set of total_tiles cells
    cells = grow_connected_cells(n, m, total_tiles, rng)

    # Decide which two become B and G; the rest are X
    b, g = far_apart_endpoints(cells, n, m, rng)

    # Build the grid
    grid = [[" " for _ in range(m)] for _ in range(n)]
    for (r, c) in cells:
        grid[r][c] = "X"
    br, bc = b
    gr, gc = g
    grid[br][bc] = "B"
    grid[gr][gc] = "G"

    # Convert to lines
    lines = []
    for r in range(n):
        row_str = "".join(grid[r])
        # Keep trailing spaces off by rstrip? In your previous format, columns matter,
        # so we *preserve* exact width m (no rstrip).
        if semicolon:
            lines.append(f"; {row_str}")
        else:
            lines.append(row_str)

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Randomly generate an n x m maze with k tiles (X) plus B and G.")
    ap.add_argument("--rows", "-n", type=int, required=True, help="Number of rows (n).")
    ap.add_argument("--cols", "-m", type=int, required=True, help="Number of columns (m).")
    ap.add_argument("--k", type=int, required=True, help="Number of regular tiles (X). B and G are added on top.")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility (optional).")
    ap.add_argument("--semicolon", action="store_true", help="Prefix each line with '; ' to match commented format.")
    args = ap.parse_args()

    maze = generate_maze(args.rows, args.cols, args.k, seed=args.seed, semicolon=args.semicolon)
    print(maze, end="")


if __name__ == "__main__":
    main()
