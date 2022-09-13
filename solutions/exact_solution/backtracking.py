import math

from helpers import cliques_from_list, is_solution


def backtrack(adj_mat, cliques, v=1, best=(math.inf, None)):
    n = adj_mat.shape[0]
    if v == n:
        if is_solution(cliques, adj_mat):
            if len(set(list(cliques)) - set({0})) < best[0]:
                best = (len(set(list(cliques))), cliques_from_list(cliques))

    else:
        for i in range(1, v + 2):
            cliques[v] = i
            if is_solution(cliques, adj_mat):
                if len(set(list(cliques)) - set({0})) < best[0]:
                    best = backtrack(adj_mat, cliques, v + 1, best)
            cliques[v] = 0
    return best
