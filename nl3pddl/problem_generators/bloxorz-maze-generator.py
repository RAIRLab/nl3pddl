"""
Simple utility to build PDDL problem files for the 'bloxorz' domain
"""

import random

def generate_bloxorz_grid(rows=10, cols=10, num_islands=6):
    """Generate a maze-like multi-island Bloxorz grid."""
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    def valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def empty(r, c):
        return valid(r, c) and grid[r][c] == "."

    def place_island(r, c, label_start, is_last=False):
        """Create a single island at (r,c) and return the upright subgoal position."""
        grid[r][c] = label_start
        orientation = random.choice(["horizontal", "vertical"])

        if orientation == "horizontal":
            pattern = [(0, 1), (0, 2), (1, 1), (1, 2)]
            goal_pos = (r, c + 3)
        else:
            pattern = [(1, 0), (2, 0), (1, 1), (2, 1)]
            goal_pos = (r + 3, c)

        for dr, dc in pattern:
            rr, cc = r + dr, c + dc
            if empty(rr, cc):
                grid[rr][cc] = "X"

        gr, gc = goal_pos
        if valid(gr, gc):
            grid[gr][gc] = "G" if is_last else "S"

        return goal_pos

    def build_bridge(r, c, direction, length):
        """Lay a straight bridge of X tiles."""
        dr, dc = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1)
        }[direction]

        for step in range(1, length + 1):
            rr, cc = r + dr * step, c + dc * step
            if empty(rr, cc):
                grid[rr][cc] = "X"

        end_r, end_c = r + dr * (length + 1), c + dc * (length + 1)
        return (end_r, end_c) if valid(end_r, end_c) else (r, c)

    # Start near top-left
    r, c = random.randint(1, 2), random.randint(1, 2)
    next_r, next_c = r, c

    for i in range(num_islands):
        label = "B" if i == 0 else "S"
        is_last = (i == num_islands - 1)
        next_r, next_c = place_island(next_r, next_c, label, is_last)
        if is_last:
            break

        # Choose a valid direction (north/south/east/west)
        for direction in random.sample(["north", "south", "east", "west"], 4):
            bridge_len = random.randint(2, 3)
            dr, dc = {
                "north": (-1, 0),
                "south": (1, 0),
                "east": (0, 1),
                "west": (0, -1)
            }[direction]
            end_r, end_c = next_r + dr * (bridge_len + 1), next_c + dc * (bridge_len + 1)
            if valid(end_r, end_c):
                next_r, next_c = build_bridge(next_r, next_c, direction, bridge_len)
                break

        # Stay within safe bounds
        next_r = max(1, min(rows - 5, next_r))
        next_c = max(1, min(cols - 5, next_c))

    return grid


def write_grid_to_file(grid, filename):
    """Write the generated grid to a text file."""
    with open(filename, "w") as f:
        for row in grid:
            f.write("".join(row) + "\n")


def generate_bloxorz_problem(data_file, output_file):
    """Build a PDDL problem file for the given Bloxorz grid text file."""
    with open(data_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    tiles = []
    start_tile = None
    goal_tile = None

    for r, line in enumerate(lines, start=1):
        for c, ch in enumerate(line, start=1):
            if ch.strip() == "":
                continue
            if ch in ("X", "B", "G", "S"):  # include S in tiles too
                tile = f"t-{r:02d}-{c:02d}"
                tiles.append((r, c))
                if ch == "B":
                    start_tile = tile
                elif ch == "G":
                    goal_tile = tile

    def tile_name(r, c):
        return f"t-{r:02d}-{c:02d}"

    adjacency = []
    tile_set = set(tiles)
    for (r, c) in tiles:
        if (r, c + 1) in tile_set:
            adjacency.append((tile_name(r, c), tile_name(r, c + 1), "east"))
            adjacency.append((tile_name(r, c + 1), tile_name(r, c), "west"))
        if (r + 1, c) in tile_set:
            adjacency.append((tile_name(r, c), tile_name(r + 1, c), "south"))
            adjacency.append((tile_name(r + 1, c), tile_name(r, c), "north"))

    problem = []
    problem.append(f"(define (problem bloxorz-prob-{data_file.split('.')[0]})")
    problem.append("    (:domain bloxorz)")
    problem.append("    (:objects")
    problem.append("        b1 - block")
    problem.append("        " + " ".join(tile_name(r, c) for (r, c) in tiles) + " - tile")
    problem.append("    )\n")

    problem.append("    (:init")
    problem.append(f"        (standing-on b1 {start_tile})")
    for t1, t2, d in adjacency:
        problem.append(f"        (adjacent {t1} {t2} {d})")
    problem.append("    )\n")

    problem.append("    (:goal (and")
    problem.append(f"        (standing-on b1 {goal_tile})")
    problem.append("    ))")
    problem.append(")")

    with open(output_file, "w") as f:
        f.write("\n".join(problem))


if __name__ == "__main__":
    random.seed(14)  # for reproducible output
    grid = generate_bloxorz_grid(num_islands=6)
    write_grid_to_file(grid, "bloxorz_grid.txt")
    print("Generated grid:")
    for row in grid:
        print("".join(row))