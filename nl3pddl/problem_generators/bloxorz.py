"""
Simple utility to build PDDL problem files for the 'bloxorz' domain
"""

def generate_bloxorz_problem_from_data(data_file, output_file):
    # Read the grid
    with open(data_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    tiles = []
    start_tile = None
    goal_tile = None

    # Parse grid: X = tile, B = start, G = goal
    for r, line in enumerate(lines, start=1):
        for c, ch in enumerate(line, start=1):
            if ch.strip() == "":
                continue
            if ch in ("X", "B", "G"):
                tile = f"t-{r:02d}-{c:02d}"
                tiles.append((r, c))
                if ch == "B":
                    start_tile = tile
                elif ch == "G":
                    goal_tile = tile

    def tile_name(r, c):
        return f"t-{r:02d}-{c:02d}"

    # Build adjacency facts
    adjacency = []
    tile_set = set(tiles)
    for (r, c) in tiles:
        # east / west
        if (r, c + 1) in tile_set:
            adjacency.append((tile_name(r, c), tile_name(r, c + 1), "east"))
            adjacency.append((tile_name(r, c + 1), tile_name(r, c), "west"))
        # north / south
        if (r + 1, c) in tile_set:
            adjacency.append((tile_name(r, c), tile_name(r + 1, c), "south"))
            adjacency.append((tile_name(r + 1, c), tile_name(r, c), "north"))

    # Build the PDDL problem
    problem = []
    problem.append(f"(define (problem bloxorz-prob-{data_file.split('.')[0]})")
    problem.append("    (:domain bloxorz)")
    problem.append("    (:objects")
    problem.append("        b1 - block")
    problem.append("        " + " ".join(tile_name(r, c) for (r, c) in tiles) + " - tile")
    problem.append("    )\n")

    # Init section
    problem.append("    (:init")
    problem.append(f"        (standing-on b1 {start_tile})")
    for t1, t2, d in adjacency:
        problem.append(f"        (adjacent {t1} {t2} {d})")
    problem.append("    )\n")

    # Goal section
    problem.append("    (:goal (and")
    problem.append(f"        (standing-on b1 {goal_tile})")
    problem.append("    ))")
    problem.append(")")

    # Write the file
    with open(output_file, "w") as f:
        f.write("\n".join(problem))