

def generate_problem(n, filename):
    n = n + 1

    num_spaces = 2 * n + 1
    spaces = [f"space{i}" for i in range(1, num_spaces + 1)]
    reds = [f"red{i}" for i in range(1, n + 1)]
    blues = [f"blue{i}" for i in range(1, n + 1)]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"(define (problem checkers-jumping-prob-{n})\n")
        f.write("  (:domain checkers-jumping)\n\n")
        f.write("  (:objects\n")
        f.write("    " + " ".join(spaces) + " - space\n")
        f.write("    " + " ".join(reds + blues) + " - checker\n")
        f.write("  )\n\n")

        f.write("  (:init\n")
        # initial placement: reds on left, empty in middle, blues on right
        for i, red in enumerate(reds):
            f.write(f"    (at {red} {spaces[i]})\n")
        f.write(f"    (empty {spaces[n]})\n")
        for i, blue in enumerate(blues):
            f.write(f"    (at {blue} {spaces[n + 1 + i]})\n")
        f.write("\n")
        # adjacency
        for i in range(num_spaces - 1):
            f.write(f"    (right-of {spaces[i]} {spaces[i + 1]})\n")
        for i in range(1, num_spaces):
            f.write(f"    (left-of {spaces[i]} {spaces[i - 1]})\n")
        f.write("\n")
        # color predicates
        for red in reds:
            f.write(f"    (is-red {red})\n")
        for blue in blues:
            f.write(f"    (is-blue {blue})\n")
        f.write("  )\n\n")

        f.write("  (:goal (and\n")
        # goal: blues
        for i, blue in enumerate(blues):
            target = spaces[i]
            f.write(f"    (at {blue} {target})\n")
        f.write(f"    (empty {spaces[n]})\n")
        # reds to rightmost
        for j, red in enumerate(reds):
            target = spaces[n + 1 + j]
            f.write(f"    (at {red} {target})\n")
        f.write("  ))\n")
        f.write(")\n")

