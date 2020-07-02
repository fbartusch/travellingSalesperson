import argparse
import logging
import time
import os
import pandas as pd

from tsp import distance
from tsp import tspsolver

"""
Module Docstring
"""


def main():
    """ Main entry point of the app """
    parser = argparse.ArgumentParser(description='Solve the travelling salesman problem.')
    installdir = os.path.dirname(__file__)
    default_input = os.path.join(installdir, "data/msg_standorte_deutschland.csv")
    parser.add_argument('-i', '--input',
                        help='Path to the input csv file.',
                        default=default_input)
    parser.add_argument('-d', '--debug',
                        help='Set logging level to debug',
                        action='store_true')
    parser.add_argument('-s', '--solver',
                        help='Choose solver: naive, nearestNeighbor, christofides (default)',
                        default='christofides')
    args = parser.parse_args()

    # Customize logger and set debug level
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Print arguments
    logging.debug("Called with arguments: " + str(args))

    # Check if input file is readable
    if not os.path.isfile(args.input):
        logging.error("File not found: " + args.input)
        exit(1)
    if not os.access(args.input, os.R_OK):
        logging.error("No permission to read: " + args.input)
        exit(1)

    # Read the input file
    logging.debug("Read input csv file")
    msg_array = pd.read_csv(args.input, delimiter=',', header=0)
    logging.debug(msg_array)

    # Build proper distance matrix
    logging.debug("Compute distance matrix")
    dist_matrix = distance.compute_distance_matrix(msg_array['Längengrad'].tolist(),
                                                   msg_array['Breitengrad'].tolist(),
                                                   method='orthodromic',
                                                   radius=6371)
    # Choose solver
    if args.solver == 'naive':
        logging.debug("Create naive solver")
        solver = tspsolver.NaiveTSPSolver(dist_matrix)
    elif args.solver == 'nearestNeighbor':
        logging.debug("Create Nearest Neighbor solver")
        solver = tspsolver.NearestNeighbor(dist_matrix)
    elif args.solver == 'christofides':
        logging.debug("Create Christofides solver")
        solver = tspsolver.Christofides(dist_matrix)
    else:
        logging.error("Unknown solver: " + args.solver)
        exit(1)

    logging.debug("Run solver...")
    starttime = time.time()
    solver.solve()
    endtime = time.time()
    runtime = endtime - starttime

    print("-----------------------")
    print("Found best solution:")
    print("\tTour: " + str(solver.solution))
    # Try to print a nicer representation of the tour if site names are available
    try:
        sites = msg_array['msg Standort'].tolist()
        s = ' -> '.join(['{}'.format(sites[v]) for v in solver.solution]) + ' ->' + sites[0]
        print("\t      {}".format(s))
    except:
        pass
    print("\tDist: {:10.2} km".format(solver.dist))
    print("\tRuntime: {:10.6f}".format(runtime) + "s")
    print("-----------------------")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
