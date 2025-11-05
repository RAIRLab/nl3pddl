"""
Simple utility to build PDDL problem files for the 'bloxorz' domain
"""

def generate_bloxorz_problem(data_file, output_file):
    # Read the grid
    with open(data_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    tiles = []
    start_tile = None
    goal_tile = None

    # Parse grid: XX = tile, II = start, GG = goal
    for r, line in enumerate(lines, start=1):
        c = 1
        while c <= len(line):
            ch = line[c-1:c+1]  # take two characters at a time
            if ch in ("XX", "II", "GG"):
                tile = f"t-{r:02d}-{c:02d}"
                tiles.append((r, c))
                if ch == "II":
                    start_tile = tile
                elif ch == "II":
                    goal_tile = tile
            c += 2  # move to next pair

    def tile_name(r, c):
        return f"t-{r:02d}-{c:02d}"

    # Build adjacency facts
    adjacency = []
    tile_set = set(tiles)
    for (r, c) in tiles:
        # east / west
        if (r, c + 2) in tile_set:  # +2 because each tile is doubled
            adjacency.append((tile_name(r, c), tile_name(r, c + 2), "east"))
            adjacency.append((tile_name(r, c + 2), tile_name(r, c), "west"))
        # north / south
        if (r + 1, c) in tile_set:
            adjacency.append((tile_name(r, c), tile_name(r + 1, c), "south"))
            adjacency.append((tile_name(r + 1, c), tile_name(r, c), "north"))

    # Build the PDDL problem
    problem = []
    problem.append(f"(define (problem bloxorz-prob-{data_file.split('.')[0]})")
    problem.append("    (:domain bloxorz)")

    # Objects section
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