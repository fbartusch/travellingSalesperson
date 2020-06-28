import itertools
import logging
import networkx
import numpy as np
import operator
from scipy.sparse.csgraph import csgraph_from_dense, minimum_spanning_tree, csgraph_to_dense, maximum_bipartite_matching


class NaiveTSPSolver:

    def __init__(self, d):
        # Distance matrix
        self.d = d
        self.num_nodes = len(self.d[0, ])
        # Solution is the ordered list of visited notes
        self.solution = []
        self.dist = float('inf')

    def solve(self):
        # If you use this for cities,  go grab a cup of coffee
        # If you use this for 7 cities, read a book
        # Take node 0 as the start
        for tour in itertools.permutations(range(1, self.num_nodes)):
            dist = self.tour_to_dist(tour)
            if dist < self.dist:
                self.solution = [0] + list(tour)
                self.dist = dist
                logging.debug("\tFound new best solution:")
                logging.debug("\t\tTour: " + str(self.solution))
                logging.debug("\t\tDist: " + str(self.dist))

    def tour_to_dist(self, x):
        return sum([self.d[x[i], x[i+1]] for i in range(len(x) - 1)]) +\
               self.d[0, x[0]] +\
               self.d[0, x[-1]]


class NearestNeighbor(NaiveTSPSolver):

    def solve(self):
        # Take node 0 as start
        self.solution = [0]
        not_visited = list(range(1, self.num_nodes))
        while len(not_visited) > 0:
            cur_node = self.solution[-1]
            # Find nearest node and update list of (not) visited nodes
            next_node = min([(i, self.d[cur_node, i]) for i in not_visited], key=operator.itemgetter(1))[0]
            self.solution.append(next_node)
            not_visited.remove(next_node)
        self.dist = self.tour_to_dist(self.solution)


class Christofides(NaiveTSPSolver):

    def solve(self):
        # https://de.wikipedia.org/wiki/Algorithmus_von_Christofides
        # 1. Get minimal spanning tree (msp)
        logging.debug("Compute minimal spanning tree ...")
        v = list(range(self.num_nodes))
        graph = csgraph_from_dense(self.d)
        msp = minimum_spanning_tree(graph)
        msp_d = csgraph_to_dense(msp)
        # Somehow the dense graph is not undirected, which is bad for the next step ...
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i == j:
                    continue
                if msp_d[i, j] == 0:
                    msp_d[i, j] = msp_d[j, i]

        # 2. Find the set of vertices with odd degree in the msp (T)
        logging.debug("Find vertices with odd degree in minimal spanning tree ...")
        odd_vertices = [i for i in v if sum([msp_d[i, j] != 0 for j in v]) % 2 == 1]

        # 3. Find a minimum-weight perfect matching M in the induced subgraph (isg) given by the set of odd vertices
        # Create adjacency matrix and take the negative values, as scipy only provides maximum weight bipartite matching
        logging.debug("Find maximum weight bipartite matching in subgraph induced by odd nodes induced ...")
        isg_d = np.zeros((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if i in odd_vertices and j in odd_vertices:
                    isg_d[i, j] = -self.d[i, j]
                    isg_d[j, i] = -self.d[i, j]
        isg_graph = csgraph_from_dense(isg_d)
        m = maximum_bipartite_matching(isg_graph)

        # 4. Combine edges of M and T (the msp) to form a connected multigraph H.
        logging.debug("Combine edges from minimal spanning tree"
                      "and the maximum weight bipartite matching to a multigraph")
        msp_m_combined = networkx.MultiGraph()
        # Add edges from the minimum spanning tree
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if msp_d[i, j] > 0:
                    msp_m_combined.add_edge(i, j, weight=msp_d[i, j])
        # Add edges from the minimum-weight perfect matching M
        m_cp = m.copy()
        for i in m:
            if i >= 0 and m_cp[m[i]] >= 0:
                msp_m_combined.add_edge(i, m[i], weight=self.d[i, m[i]])
                # Do not add the same edge twice
                m_cp[m[i]] = -1
                m_cp[i] = -1

        # 5. Find Eulerian circuit in H, starting at node 0
        logging.debug("Find an eulerian path in the multigraph starting at vertice 0")
        eulerian_path = networkx.eulerian_path(msp_m_combined, source=0)

        # 6. Make the circuit found in previous step into a Hamiltonian circuit
        # Follow the eulerian path and replace already visited vertices by an edge to the next not yet visited vertice.
        logging.debug("Convert eulerarian path to hamiltonian circuit")
        first_edge = next(eulerian_path)
        self.solution = [first_edge[0], first_edge[1]]
        for e in eulerian_path:
            if e[1] in self.solution:
                continue
            else:
                self.solution.append(e[1])
        self.dist = self.tour_to_dist(self.solution)
