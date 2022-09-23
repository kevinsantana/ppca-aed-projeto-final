import time

from loguru import logger


class BranchAndBound:
    """
    The maximum clique in a graph can be found by computing the largest clique containing
    each vertex and picking the largest among these. A key element of our exact algorithm is
    that during the search for the largest clique containing a given vertex, vertices that cannot
    form cliques larger than the current maximum clique are pruned, in a hierarchical fashion.

    The exact algorithm examines for every vertex vi all relevant cliques containing the vertex
    vi in order to determine the clique of maximum size among them.
    """

    def __init__(self, lb=0):
        self.lb = lb

        self.best_clique = []
        self.cur_max = 0

    def Clique(self, graph, U, size, cur_clique):
        """
        The subroutine CLIQUE goes through every relevant clique containing vi in a recursive
        fashion and returns the largest.
        Pruning #4: checks for the case where even if all vertices of U were added to get a clique, its size would not
        exceed that of the largest clique encountered so far in the search, max.
        Pruning #5: reduces the number of comparisons needed to generate the intersection

        :param graph: graph where cliques will be searched.
        :param U: neighbor list U for a vertex v
        :param size: size of the clique found at any point through the recursion.
        :param cur_clique: current clique at a point through the recursion.
        """
        if len(U) == 0:
            if size > self.cur_max:
                self.cur_max = size
                self.best_clique = cur_clique
            return

        while len(U) > 0:
            if size + len(U) <= self.cur_max:  # pruning 4
                return

            vertex = U.pop()
            new_cur_clique = cur_clique[:]
            new_cur_clique.append(vertex)

            # pruning 5
            neib_vertex = set(v for v in graph[vertex] if len(graph[v]) >= self.cur_max)
            new_U = U.intersection(neib_vertex)

            self.Clique(graph, new_U, size + 1, new_cur_clique)

    def MaxClique(self, graph, lb=0):
        """
        The main routine MAXCLIQUE generates for each vertex vi e V a
        set U c N (vi) (neighbors of vi that survive pruning) and calls the subroutine CLIQUE on U

        Pruning #1: ilters vertices having strictly fewer neighbors than the size of themaximum clique already computed
        Pruning #2: While forming the neighbor list U for a vertex vi, we include only those of vis neighbors for which
        the largest clique containing them has not been found
        Pruning #3: excludes vertices vj e N (vi) that have degree less than the current value of max, since any such
        vertex could not form a clique of size larger than max
        """
        # nodes are labeled as 1, 2, ....no_of_vertices
        no_of_vertices = len(graph)
        self.cur_max = lb
        self.best_clique = []

        for i in range(1, no_of_vertices + 1):
            if str(i) not in graph:
                continue
            neib_vi = graph[str(i)]

            if len(neib_vi) >= self.cur_max:  # pruning 1
                U = set()
                cur_clique = [str(i)]

                for j in neib_vi:
                    if int(j) > i:  # pruning 2
                        if len(graph[j]) >= self.cur_max:  # pruning 3
                            U.add(j)

                self.Clique(graph, U, 1, cur_clique)

    def run(self, graph):
        start_time = time.time()
        self.MaxClique(graph, self.lb)
        end_time = time.time()

        s = self.cur_max
        t = (end_time - start_time) * 1000

        logger.info(f"clique size: {s}, time(ms): {t:.3f}")
        return (s, t)
