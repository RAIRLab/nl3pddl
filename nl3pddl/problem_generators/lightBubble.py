import random

def generate_problem(v, filename):

    v += 2
    num_bubbles = min(10, v)
    num_steps = v + random.randint(1, v)
    
    # Create bubble names
    bubbles = [f"b{i+1}" for i in range(num_bubbles)]

    # Generate a random graph with kmax=3
    neighbors = {b: set() for b in bubbles}
    

    for b in bubbles:
        k = random.randint(1, min(3, num_bubbles - 1))  # target degree 1–3

        # keep adding neighbors until reaching desired degree or no valid options remain
        attempts = 0
        while len(neighbors[b]) < k:
        # get candidates that are not self and have <3 neighbors
            candidates = [n for n in bubbles if n != b and len(neighbors[n]) < 3 and n not in neighbors[b]]
            if not candidates:
             # no valid neighbor left → stop to avoid infinite loop
                break

            n = random.choice(candidates)
            neighbors[b].add(n)
            neighbors[n].add(b)

            attempts += 1
            if attempts > 100:  # safeguard fallback
                break

    # Initialize all bubbles to OFF (goal state)
    states = {b: "off" for b in bubbles}

    # Apply inverse operations (presses)
    for _ in range(num_steps):
        b = random.choice(bubbles)
        # toggle all neighbors
        for n in neighbors[b]:
            states[n] = "on" if states[n] == "off" else "off"

    allOffInitialy = 1
    for b in bubbles: 
        if states[b] == "on" : allOffInitialy = 0

    if(allOffInitialy):
        randBubble = random.choice(bubbles)
        for n in neighbors[randBubble]:
            states[n] = "on" if states[n] == "off" else "off"

    # Generate PDDL problem file
    with open(filename, "w") as f:
        f.write(f"(define (problem lights_out_{num_bubbles}_{num_steps})\n")
        #print(f"(define (problem lights_out_{num_bubbles}_{num_steps})\n")
        f.write("  (:domain lights-out-strips)\n")
        #print("  (:domain lights-out-strips)\n")
        # Objects
        f.write("  (:objects\n")
        #print("  (:objects\n")
        for b in bubbles:
            f.write(f"    {b} - bubble\n")
            #print(f"    {b} - bubble\n")
        f.write("  )\n")
        #print("  )\n")

        # Initial state
        f.write("  (:init\n")
        #print("  (:init\n")
        for b in bubbles:
            f.write(f"    ({states[b]} {b})\n")
            #print(f"    ({states[b]} {b})\n")
        # Connections
        for b, ns in neighbors.items():
            for n in ns:
                f.write(f"    (connected {b} {n})\n")
                #print(f"    (connected {b} {n})\n")
                #f.write(f"    (connected {n} {b})\n")
        # Neighbor countsx
        for b, ns in neighbors.items():
            count = len(ns)
            if count == 1:
                f.write(f"    (one-neighbor {b})\n")
                #print(f"    (one-neighbor {b})\n")
            elif count == 2:
                f.write(f"    (two-neighbors {b})\n")
                #print(f"    (two-neighbors {b})\n")
            elif count == 3:
                f.write(f"    (three-neighbors {b})\n")
                #print(f"    (three-neighbors {b})\n")
        f.write("  )\n")
        #print("  )\n")

        # Goal: all OFF
        f.write("  (:goal (and\n")
        #print("  (:goal (and\n")
        for b in bubbles:
            f.write(f"    (off {b})\n")
            #print(f"    (off {b})\n")
        f.write("  ))\n")
        #print("  ))\n")

        f.write(")\n")
        #print(")\n")

    #print(f"PDDL problem generated: {filename}")

if __name__ == "__main__":
        generate_problem(10, f"../../data/domains/light-bubble/problem_example.pddl")

