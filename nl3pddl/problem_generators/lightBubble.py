import random

def generate_problem(num_bubbles=6, num_steps=10, filename="lights_out_problem.pddl"):
    
    # Create bubble names
    bubbles = [f"b{i+1}" for i in range(num_bubbles)]

    # Generate a random graph with kmax=3
    neighbors = {b: set() for b in bubbles}
    for b in bubbles:
        k = random.randint(1, min(3, num_bubbles-1))  # 1..3 neighbors
        while len(neighbors[b]) < k:
            n = random.choice(bubbles)
            if n != b:
                neighbors[b].add(n)
                neighbors[n].add(b)  # undirected

    # Initialize all bubbles to OFF (goal state)
    states = {b: "off" for b in bubbles}

    # Apply inverse operations (presses)
    for _ in range(num_steps):
        b = random.choice(bubbles)
        # toggle all neighbors
        for n in neighbors[b]:
            states[n] = "on" if states[n] == "off" else "off"

    # Generate PDDL problem file
    with open(filename, "w") as f:
        f.write(f"(define (problem lights_out_{num_bubbles})\n")
        f.write("  (:domain lights-out-strips)\n")
        # Objects
        f.write("  (:objects\n")
        for b in bubbles:
            f.write(f"    {b} - bubble\n")
        f.write("  )\n")

        # Initial state
        f.write("  (:init\n")
        for b in bubbles:
            f.write(f"    ({states[b]} {b})\n")
        # Connections
        for b, ns in neighbors.items():
            for n in ns:
                f.write(f"    (connected {b} {n})\n")
                #f.write(f"    (connected {n} {b})\n")
        # Neighbor counts
        for b, ns in neighbors.items():
            count = len(ns)
            if count == 1:
                f.write(f"    (one-neighbor {b})\n")
            elif count == 2:
                f.write(f"    (two-neighbors {b})\n")
            elif count == 3:
                f.write(f"    (three-neighbors {b})\n")
        f.write("  )\n")

        # Goal: all OFF
        f.write("  (:goal (and\n")
        for b in bubbles:
            f.write(f"    (off {b})\n")
        f.write("  ))\n")

        f.write(")\n")

    print(f"PDDL problem generated: {filename}")

if __name__ == "__main__":
    generate_problem()

