from unittest import TestCase
import numpy as np

from tsp.tspsolver import NaiveTSPSolver
from tsp.tspsolver import NearestNeighbor
from tsp.tspsolver import Christofides


class TestTSPSolver(TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        # From: https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
        self.d = np.array([[0.0, 3.0, 4.0, 2.0, 7.0],
                      [3.0, 0.0, 4.0, 6.0, 3.0],
                      [4.0, 4.0, 0.0, 5.0, 8.0],
                      [2.0, 6.0, 5.0, 0.0, 6.0],
                      [7.0, 3.0, 8.0, 6.0, 0.0]])

    def test_naive(self):
        solver = NaiveTSPSolver(self.d)
        solver.solve()
        self.assertEqual(solver.dist, 19)
        self.assertEqual(solver.solution, [0, 2, 1, 4, 3])

    def test_nearest_neighbor(self):
        solver = NearestNeighbor(self.d)
        solver.solve()
        self.assertEqual(solver.dist, 21)
        self.assertEqual(solver.solution, [0, 3, 2, 1, 4])

    def test_christofides(self):
        solver = Christofides(self.d)
        solver.solve()
        self.assertEqual(solver.dist, 21)
        self.assertEqual(solver.solution, [0, 2, 3, 4, 1])
