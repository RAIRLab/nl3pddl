"""
This file contains the driver for the NL3PDDL project.
"""

import argparse

import nl3pddl as n3p

# Based on args, if -g is passed, generate problems
# if -l is passed, generate landmarks
# if -r is passed, run the experiment, note that all three can be run in tandem
# but not -l and -r together
# if no arguments are passed treat it as -r and run the experiment
# if -i is passed, generate the graph image of the experiment
# if -p is passed, plot all figures
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

    args = parser.parse_args()

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

    if not (args.generate or args.landmarks or args.run or args.image or args.plot):
        print("No arguments passed, running the experiment by default.")
        #n3p.generate_landmarks()
        n3p.run_experiment()
        #n3p.plot_all_figures()

