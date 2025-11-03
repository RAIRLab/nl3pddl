#!/usr/bin/env python3
"""
Generate a PDDL problem file for the 'bloxorz' domain from a text maze.

Maze legend:
  X - walkable tile
  B - start tile (block initially stands here)
  G - goal tile

Supports ragged rows and leading spaces (columns are 1-based and preserved).
If most lines begin with ';', the script strips a leading ';' and any following spaces.

Usage:
  python maze_to_pddl.py -i maze.txt -o p01.pddl --problem p01 --domain bloxorz

If -i is omitted, reads from STDIN. If -o is omitted, prints to STDOUT.
"""

from __future__ import annotations
import argparse
import sys
from typing import Dict, List, Set, Tuple

Coord = Tuple[int, int]

PERPENDICULAR_FACTS = [
    ("north", "east"),
    ("north", "west"),
    ("east", "north"),
    ("west", "north"),
    ("south", "east"),
    ("south", "west"),
    ("east", "south"),
    ("west", "south"),
]


def _maybe_strip_comment_semicolon(lines: List[str]) -> List[str]:
    """If most non-empty lines start with ';', strip leading ';' and spaces."""
    content_lines = [ln.rstrip("\n") for ln in lines if ln.strip("\n") != ""]
    if not content_lines:
        return []

    semis = sum(1 for ln in content_lines if ln.lstrip().startswith(";"))
    # Heuristic: if at least half the lines start with ';', strip them.
    strip = semis >= (len(content_lines) / 2)

    processed = []
    for ln in lines:
        s = ln.rstrip("\n")
        if strip:
            # Find first ';' if present after any leading spaces
            lstripped = s.lstrip()
            if lstripped.startswith(";"):
                # Remove up to and including the first ';' in the original string
                # Then lstrip spaces that follow it (to handle "; XXX" -> "XXX")
                first_semicolon_index = s.find(";")
                s = s[first_semicolon_index + 1 :].lstrip()
        processed.append(s)
    return processed


def parse_maze_text(maze_text: str) -> Tuple[Set[Coord], Coord, Coord, int, int]:
    """
    Parse the maze text and return:
      tiles: set of (r, c) coords with tiles
      start: (r, c) for 'B'
      goal:  (r, c) for 'G'
      max_r: number of rows actually present (based on input lines)
      max_c: max column index seen across all rows
    """
    raw_lines = maze_text.splitlines()
    lines = _maybe_strip_comment_semicolon(raw_lines)
    # Keep blank lines out of the grid; retain leading spaces on meaningful lines
    lines = [ln for ln in lines if ln.strip() != ""]

    tiles: Set[Coord] = set()
    start: Coord | None = None
    goal: Coord | None = None

    max_c = 0
    for r, line in enumerate(lines, start=1):
        # Keep exact character positions (including leading spaces)
        for c, ch in enumerate(line, start=1):
            if ch in {"X", "B", "G"}:
                tiles.add((r, c))
                max_c = max(max_c, c)
                if ch == "B":
                    if start is not None:
                        raise ValueError("Multiple 'B' (start) tiles found.")
                    start = (r, c)
                elif ch == "G":
                    if goal is not None:
                        raise ValueError("Multiple 'G' (goal) tiles found.")
                    goal = (r, c)

    if start is None:
        raise ValueError("No 'B' (start) tile found in the maze.")
    if goal is None:
        raise ValueError("No 'G' (goal) tile found in the maze.")

    max_r = len(lines)
    return tiles, start, goal, max_r, max_c


def tname(r: int, c: int, w: int) -> str:
    """Tile name as t-rr-cc using zero-padded width w (>=2)."""
    return f"t-{r:0{w}d}-{c:0{w}d}"


def build_adjacencies(tiles: Set[Coord]) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    """
    Build directed adjacency lists:
      horizontal: list of (tile_a, tile_b, 'east' or 'west')
      vertical:   list of (tile_a, tile_b, 'south' or 'north')
    We only generate east and south (forward) and mirror them as west/north.
    """
    tile_set = set(tiles)
    # We'll fill these in the caller once we know the tile naming width.
    # Here we only compute coordinate pairs.
    east_edges: List[Tuple[Coord, Coord]] = []
    south_edges: List[Tuple[Coord, Coord]] = []

    for (r, c) in sorted(tile_set):
        if (r, c + 1) in tile_set:
            east_edges.append(((r, c), (r, c + 1)))
        if (r + 1, c) in tile_set:
            south_edges.append(((r, c), (r + 1, c)))

    return east_edges, south_edges


def format_pddl(
    tiles: Set[Coord],
    start: Coord,
    goal: Coord,
    problem_name: str = "p01",
    domain_name: str = "bloxorz",
) -> str:
    """
    Produce the PDDL problem text.
    """
    if not tiles:
        raise ValueError("No tiles to export.")

    max_r = max(r for r, _ in tiles)
    max_c = max(c for _, c in tiles)
    width = max(2, len(str(max_r)), len(str(max_c)))

    # Group tiles by row for cleaner object listing
    rows: Dict[int, List[int]] = {}
    for r, c in tiles:
        rows.setdefault(r, []).append(c)
    for r in rows:
        rows[r].sort()

    # Build edges (in terms of coords), then convert to names
    east_edges, south_edges = build_adjacencies(tiles)

    def tn(rc: Coord) -> str:
        return tname(rc[0], rc[1], width)

    # Objects section (row-wise, matching your example style)
    obj_lines: List[str] = []
    obj_lines.append("(:objects B - block")
    tiles = []
    for r in sorted(rows.keys()):
        cols = rows[r]
        if not cols:
            continue
        names = [tn((r, c)) for c in cols]
        tiles.extend(names)
        # Put each row on its own line for readability
        obj_lines.append("    " + " ".join(names))
    obj_lines[-1] += "  - tile)"  # attach type to final tile line

    # Init section
    init_lines: List[str] = []
    # Perpendicular facts
    for d1, d2 in PERPENDICULAR_FACTS:
        init_lines.append(f"  (perpendicular {d1} {d2})")

    # Horizontal adjacencies (east then west)
    for (a, b) in east_edges:
        init_lines.append(f"  (adjacent {tn(a)} {tn(b)} east)")
    # Vertical adjacencies (south)
    for (a, b) in south_edges:
        init_lines.append(f"  (adjacent {tn(a)} {tn(b)} south)")

    # Opposite directions
    # For every east edge a->b, add west b->a
    for (a, b) in east_edges:
        init_lines.append(f"  (adjacent {tn(b)} {tn(a)} west)")
    # For every south edge a->b, add north b->a
    for (a, b) in south_edges:
        init_lines.append(f"  (adjacent {tn(b)} {tn(a)} north)")

    for t in tiles:
        init_lines.append(f"  (active {t})")

    # Start position
    init_lines.append(f"\n  (standing-on B {tn(start)})")


    init_block = "(:init\n" + "\n".join(init_lines) + "\n)"

    # Goal
    goal_block = f"(:goal (and \n  (standing-on B {tn(goal)})\n))"

    # Top-level
    lines: List[str] = []
    lines.append(f"(define (problem {problem_name})")
    lines.append(f"  (:domain {domain_name})")
    lines.append("  ; t-r-c describes tile in row r column c")
    lines.append("  ;")
    lines.append("  " + "\n  ".join(obj_lines))
    lines.append("")
    lines.append("  " + init_block.replace("\n", "\n  "))
    lines.append("")
    lines.append("  " + goal_block.replace("\n", "\n  "))
    lines.append(")")

    return "\n".join(lines) + "\n"


def generate_pddl_from_maze(
    maze_text: str,
    problem_name: str = "p01",
    domain_name: str = "bloxorz",
) -> str:
    tiles, start, goal, _, _ = parse_maze_text(maze_text)
    return format_pddl(tiles, start, goal, problem_name, domain_name)


def main():
    ap = argparse.ArgumentParser(description="Convert a text maze to a PDDL problem (bloxorz domain).")
    ap.add_argument("-i", "--input", type=str, default=None, help="Path to input maze text file",required=True)
    ap.add_argument("-o", "--output", type=str, default=None, help="Path to write PDDL file (default: STDOUT)")
    ap.add_argument("--problem", type=str, default="p01", help="PDDL problem name (default: p01)")
    ap.add_argument("--domain", type=str, default="bloxorz", help="PDDL domain name (default: bloxorz)")
    args = ap.parse_args()

    # Read maze text
    with open(args.input, "r", encoding="utf-8") as f:
        maze_text = f.read()

    try:
        pddl = generate_pddl_from_maze(maze_text, problem_name=args.problem, domain_name=args.domain)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(pddl)
    else:
        print(pddl)


if __name__ == "__main__":
    main()
