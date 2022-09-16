import random

from solutions.heuristics.ant_colony_optimization import read_graph


def greedy_search(graph):
    """
    In greedy approach of finding a single maximal clique we start with any Starting with an arbitrary clique (for
    instance, any single vertex or even the empty set), grow the current clique one vertex at a time by looping through
    the graph's remaining vertices.

    For each vertex v that this loop examines, add v to the clique if it is adjacent to every vertex that is already in
    the clique, and discard v otherwise. The maximal clique can be different if we start with differnet vertex as a graph
    may have more than one maximal clique.

    Start from an arbitrary vertex
    Given a clique of size, repeat:
        - Add a vertex randomly from the common neighbors of the existing clique
        - If there is no common neighbors, stop and return the clique
    """
    clique = []
    vertices = list(graph.keys())
    rand = random.randrange(0, len(vertices), 1)
    clique.append(vertices[rand])

    for v in vertices:

        if v in clique:
            continue

        is_next = True
        for u in clique:

            if u in graph[v]:
                continue
            else:
                is_next = False
                break

        if is_next:
            clique.append(v)

    return sorted(clique)
