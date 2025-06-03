"""
Generate PDDL problems for a flow problem using 
Using the flow pddl problem generator from 
https://github.com/James-Oswald/Flow-Free-PDDL
and the problem generator from
https://github.com/thomasahle/numberlink
in our submodules
"""

import subprocess
import sys
from pathlib import Path


def problem_gen(
    n: int, m: int,
    flows: dict[str, tuple[tuple[int, int], tuple[int, int]]]
) -> str:
    """
    Given the dimensions and a map from the color to the starting
    and ending points of the flows, generate a PDDL problem for
    the flow problem.
    """
    points = []
    connections = []
    for i in range(n):
        for j in range(m):
            points.append(f"p_{i}_{j}")
            if i < n-1:
                connections.append((f"p_{i}_{j}", f"p_{i+1}_{j}"))
            if j < m-1:
                connections.append((f"p_{i}_{j}", f"p_{i}_{j+1}"))
            if i > 0:
                connections.append((f"p_{i}_{j}", f"p_{i-1}_{j}"))
            if j > 0:
                connections.append((f"p_{i}_{j}", f"p_{i}_{j-1}"))
    colors = []
    color_locs = []
    for color, ((x1, y1), (x2, y2)) in flows.items():
        assert not " " in color
        colors.append(color)
        assert 0 <= x1 < n and 0 <= y1 < m
        color_locs.append((color, f"p_{x1}_{y1}"))
        assert 0 <= x2 < n and 0 <= y2 < m
        color_locs.append((color, f"p_{x2}_{y2}"))

    nl = "\n\t"
    return f'''
(define (problem flow_{n}_{m}) (:domain flow_free)
(:objects 
    {nl.join(colors)} - color
    {nl.join(points)} - location
)

(:init
    (offboard)
    {nl.join(f"(empty {p})" for p in points)}
    {nl.join(f"(adjacent {x} {y})" for (x,y) in connections)}
    {nl.join(f"(flow-end {l} {c})" for (c, l) in color_locs)}
)

(:goal (and
    ;We avoid using forall due to the translator implementation generating axioms which 
    ;make it so we can't use many good planner heuristics.
    ;(forall (?c - color) (flow-complete ?c))
    ;(forall (?l - location) (not-empty ?l))
    {nl.join(f"(flow-complete {c})" for c in colors)}
    {nl.join(f"(not-empty {p})" for p in points)}
))

)'''


def gen_problem_file(
    n: int, m: int,
    flows: dict[str, tuple[tuple[int, int], tuple[int, int]]],
    name=None
) -> None:
    """
    Generate a PDDL problem file for a flow problem with the given
    dimensions and flows.
    """
    if name is None:
        name = f"flowproblem{n}x{m}.pddl"
    with open(name, "w", encoding="utf-8") as file:
        file.write(problem_gen(n, m, flows))


def generate_flow_problem(width: int, height: int) -> str:
    """
    Generate a flow problem using the numberlink generator.
    Returns the standard output as a string.
    """
    gen_script_path = Path("submodules") / "numberlink" / "gen" / "gen.py"
    try:
        result = subprocess.run(
            [
                sys.executable, str(gen_script_path),
                str(width), str(height), "1"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error generating flow problem: {e.stderr}") from e


def parse_flow_problem(problem_str: str) \
        -> dict[str, tuple[tuple[int, int], tuple[int, int]]]:
    """
    Parse the flow problem string and return a 
    dictionary mapping colors to their start and end coordinates.
    """
    lines = problem_str.strip().splitlines()
    starts = {}
    ends = {}
    for i, line in enumerate(lines[1:]):
        for j, c in enumerate(line):
            if c == '.':
                continue
            if c in starts and c in ends:
                raise ValueError(
                    f"Color {c} appears more than twice in the problem.")
            elif c in starts and c not in ends:
                ends[c] = (i, j)
            elif c not in starts and c not in ends:
                starts[c] = (i, j)
            else:
                raise ValueError("should never happen")
    assert len(starts) == len(ends)
    rv = {}
    for color, _ in starts.items():
        if color not in ends:
            raise ValueError(f"Color {color} has no end point.")
        rv[color] = (starts[color], ends[color])
    return rv

def main():
    """
    Main
    """
    width = 5
    height = 5
    problem_str = generate_flow_problem(width, height)
    flows = parse_flow_problem(problem_str)

    # Generate the PDDL problem file
    gen_problem_file(width, height, flows, "flow_problem.pddl")

    print("Flow problem generated and saved to flow_problem.pddl")

if __name__ == "__main__":
    main()
