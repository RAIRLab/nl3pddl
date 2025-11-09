"""
This file contains the driver for the NL3PDDL project.
"""

import resource

import argparse
import nl3pddl as n3p

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NL3PDDL Driver")
    parser.add_argument(
        "-g", "--generate", action="store_true",
        help="Generate problems for the NL3PDDL project"
    )
    parser.add_argument(
        "-l", "--landmarks", action="store_true",
        help="Generate landmarks for the NL3PDDL project"
    )
    parser.add_argument(
        "-r", "--run", action="store_true",
        help="Run the NL3PDDL experiment"
    )
    parser.add_argument(
        "-i", "--image", action="store_true",
        help="Generate the graph image of the experiment"
    )
    parser.add_argument(
        "-p", "--plot", action="store_true",
        help="Plot all figures"
    )
    parser.add_argument(
        "-t", "--test", nargs="*", metavar=("GENERATOR", "SIZE"),
        help="Test problem generators. Use -t to test all, -t <generator> to test one, or -t <generator> <size> to test with specific size"
    )

    args = parser.parse_args()

    # changing hard limit on open FD, sockets, pipes etc
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (65535, hard))

    if args.generate:
        n3p.generate_problems()

    if args.landmarks:
        n3p.generate_landmarks()

    if args.run:
        n3p.run_experiment()

    if args.image:
        n3p.graph_pipeline_image()

    if args.plot:
        n3p.plot_all_figures()

    if args.test is not None:
        if len(args.test) == 0:
            # No arguments: test all generators
            n3p.test_generators()
        elif len(args.test) == 1:
            # One argument: test specific generator with default size
            n3p.test_generators(generator_name=args.test[0])
        else:
            # Two arguments: test specific generator with specific size
            n3p.test_generators(generator_name=args.test[0], problem_size=int(args.test[1]))

    if not (args.generate or args.landmarks or args.run or args.image or args.plot or args.test is not None):
        print("No arguments passed, running the experiment by default.")
        #n3p.generate_landmarks()
        n3p.run_experiment()
        #n3p.plot_all_figures()
