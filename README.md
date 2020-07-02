# Travelling Salesperson

An implementation of two heuristics for the <a href="https://www.get-in-it.de/coding-challenge" target="_blank">Get in IT coding challenge</a>.

## Installation

Clone this repo and the package and dependencies via `pip`.
The package is tested on Ubuntu 18.04.

```
# Create an optional conda environment
conda create --name tsp python=3.7
conda activate tsp

git clone https://github.com/fbartusch/travellingSalesperson.git
cd travellingSalesperson
pip install .
```

## Features

The package implements three algorithms for the Travelling Salesperson problem.

* Brute-Force (not recommended for more than 6 cities)
* Nearest Neighbor (very fast heuristic, but the solution can be very bad)
* Christofides algorithm (default, fast heuristic yields a solution within 3/2 of the optimum)

## Usage / Solution

```
$ tsp
-----------------------
Found best solution:
	Tour: [0, 16, 8, 4, 1, 2, 10, 9, 17, 13, 14, 6, 5, 12, 7, 20, 3, 19, 18, 15, 11]
	      Ismaning/München (Hauptsitz) -> Passau -> Görlitz -> Chemnitz -> Berlin -> Braunschweig -> Hannover -> Hamburg -> Schortens/Wilhelmshaven -> Lingen (Ems) -> Münster -> Essen -> Düsseldorf -> Köln/Hürth -> Frankfurt -> Walldorf -> Bretten -> Stuttgart -> St. Georgen -> Nürnberg -> Ingolstadt -> Ismaning/München (Hauptsitz)
	Dist: 2418.126530555129
	Runtime:   0.003140s
-----------------------
```

## Help

```
tsp -h
usage: tsp [-h] [-i INPUT] [-d] [-s SOLVER]

Solve the travelling salesman problem.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input csv file.
  -d, --debug           Set logging level to debug
  -s SOLVER, --solver SOLVER
                        Choose solver: naive, nearestNeighbor, christofides
                        (default)

```
