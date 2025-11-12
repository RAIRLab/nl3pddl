import random
from copy import deepcopy


def generate_full_4x4_sudoku():
    """Generate a fully solved 4x4 Sudoku grid."""
    grid = [[0 for _ in range(4)] for _ in range(4)]

    def check_grid(g):
        return all(0 not in row for row in g)

    def fill_grid(g):
        for i in range(16):
            r, c = i // 4, i % 4
            if g[r][c] == 0:
                nums = [1, 2, 3, 4]
                random.shuffle(nums)
                for val in nums:
                    if val not in g[r] and val not in [g[x][c] for x in range(4)]:
                        sr, sc = (r // 2) * 2, (c // 2) * 2
                        square = [g[x][sc:sc + 2] for x in range(sr, sr + 2)]
                        if val not in (square[0] + square[1]):
                            g[r][c] = val
                            if check_grid(g) or fill_grid(g):
                                return True
                break
        g[r][c] = 0
        return False

    fill_grid(grid)
    return grid

def is_valid_partial(grid):
    """Return True if every empty cell has at least one possible candidate."""
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                possible = {1, 2, 3, 4}
                # Remove row and col values
                possible -= set(grid[r])
                possible -= {grid[x][c] for x in range(4)}
                # Remove box values
                sr, sc = (r // 2) * 2, (c // 2) * 2
                for x in range(sr, sr + 2):
                    for y in range(sc, sc + 2):
                        possible.discard(grid[x][y])
                if not possible:
                    return False
    return True

def generate_valid_4x4_sudoku():
    """Generate a valid 4x4 Sudoku puzzle with one clue per number."""
    while True:
        grid = generate_full_4x4_sudoku()

        # Keep only one of each number (1–4)
        keep_positions = []
        for num in range(1, 5):
            cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == num]
            pos = random.choice(cells)
            keep_positions.append(pos)

        # Create the puzzle
        puzzle = deepcopy(grid)
        for r in range(4):
            for c in range(4):
                if (r, c) not in keep_positions:
                    puzzle[r][c] = 0

        # Validate the puzzle (each empty has at least one possible candidate)
        if is_valid_partial(puzzle):
            return puzzle

def generate_sudoku_problem(_, output_file, seed=None):
    grid_size = 4

    if seed is not None:
        random.seed(seed)

    digits = [1, 2, 3, 4]
    num_names = ["one", "two", "three", "four"]
    rows = [f"r{i}" for i in range(1, grid_size + 1)]
    cols = [f"c{i}" for i in range(1, grid_size + 1)]
    boxes = [f"b{i}" for i in range(1, grid_size + 1)]
    positions = [f"p{r}{c}" for r in range(1, grid_size + 1) for c in range(1, grid_size + 1)]

    # Generate a valid grid
    grid = generate_valid_4x4_sudoku()

    # Start building PDDL text
    problem = "(define (problem sudoku)\n"
    problem += "  (:domain sudoku)\n\n"

    # Objects
    problem += "  (:objects\n"
    problem += "    " + " ".join(positions) + " - pos\n"
    problem += "    " + " ".join(rows) + " - row\n"
    problem += "    " + " ".join(cols) + " - col\n"
    problem += "    " + " ".join(boxes) + " - box\n"
    problem += "    " + " ".join(num_names) + " - number\n"
    problem += "  )\n\n"

    # Init section
    problem += "  (:init\n"
    for r in range(grid_size):
        for c in range(grid_size):
            pos = f"p{r+1}{c+1}"
            row = f"r{r+1}"
            col = f"c{c+1}"
            box = f"b{(r // 2) * 2 + (c // 2) + 1}"
            problem += f"    (posdata {pos} {row} {col} {box})\n"

    filled_positions = set()
    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] != 0:
                pos = f"p{r+1}{c+1}"
                num = num_names[grid[r][c] - 1]
                row = f"r{r+1}"
                col = f"c{c+1}"
                box = f"b{(r // 2) * 2 + (c // 2) + 1}"

                # Mark filled cell
                problem += f"    (filled {pos})\n"
                filled_positions.add(pos)

                # Sudoku rule constraints
                #problem += f"    (not (not-in-row {num} {row}))\n"
                #problem += f"    (not (not-in-col {num} {col}))\n"
                #problem += f"    (not (not-in-box {num} {box}))\n"

                for other_r in rows:
                    if other_r != row:
                        problem += f"    (not-in-row {num} {other_r})\n"
                for other_c in cols:
                    if other_c != col:
                        problem += f"    (not-in-col {num} {other_c})\n"
                for other_b in boxes:
                    if other_b != box:
                        problem += f"    (not-in-box {num} {other_b})\n"

    # Mark empty positions
    for pos in positions:
        if pos not in filled_positions:
            problem += f"    (empty {pos})\n"

    problem += "  )\n\n"

    # Goal
    problem += "  (:goal (and\n"
    for pos in positions:
        problem += f"    (filled {pos})\n"
    problem += "  ))\n"
    problem += ")\n"

    # Write to file
    with open(output_file, "w") as f:
        f.write(problem)

    # For debugging: show generated grid
    print("Generated Sudoku grid (0 = empty):")
    for row in grid:
        print(row)


if __name__ == "__main__":
    generate_sudoku_problem("example_generated.pddl")