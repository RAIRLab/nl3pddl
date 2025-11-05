import argparse

def generate_hanoi_problem(n, filename):
    
    pegs = ["peg1", "peg2", "peg3"]
    disks = [f"d{i}" for i in range(1, n + 1)]

    with open(filename, "w") as f:
        f.write(f"(define (problem hanoi-{n})\n")
        f.write("  (:domain towers-of-hanoi)\n\n")

        # Objects
        f.write("  (:objects\n")
        f.write("    " + " ".join(disks) + " - disk\n")
        f.write("    " + " ".join(pegs) + " - peg\n")
        f.write("  )\n\n")

        # Init
        f.write("  (:init\n")

        # Disk sizes (smaller relationships)
        for i in range(n):
            for j in range(i + 1, n):
                f.write(f"    (smaller {disks[j]} {disks[i]})\n")
        f.write("\n")


        # Initial stack: all on peg1, in size order (largest at bottom)
        for i in range(n):
            if i == 0:
                # bottom disk on peg1
                f.write(f"    (on {disks[i]} peg1)\n")
            else:
                # smaller disk on top of previous one
                f.write(f"    (on-top {disks[i]} {disks[i-1]})\n")
                f.write(f"    (on {disks[i]} {disks[i-1]})\n")

        # Clear top disk and clear other pegs
        f.write(f"    (clear-disk {disks[-1]})\n")
        f.write(f"    (clear-peg peg2)\n")
        f.write(f"    (clear-peg peg3)\n")
        f.write("  )\n\n")

        # All disks moved to peg3 in the same order
        f.write("  (:goal\n")
        f.write("    (and\n")
        for i in range(n):
            if i == 0:
                f.write(f"      (on {disks[i]} peg3)\n")
            else:
                f.write(f"      (on-top {disks[i]} {disks[i-1]})\n")
                f.write(f"      (on {disks[i]} {disks[i-1]})\n")
        f.write(f"      (clear-disk {disks[-1]})\n")
        f.write("    )\n")
        f.write("  )\n")
        f.write(")\n")


if __name__ == "__main__":
    generate_hanoi_problem(4, "problem_generated.pddl")
