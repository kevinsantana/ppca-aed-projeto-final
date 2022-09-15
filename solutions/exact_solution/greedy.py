import random

from solutions.heuristics.ant_colony_optimization import read_graph


def greedy_search(graph):
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
