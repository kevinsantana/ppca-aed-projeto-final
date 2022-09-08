import math
import time

from test_instances import test_graph1
from helpers import cliques_from_list, is_solution


def backtrack(adj_mat, cliques, v=1,  best=(math.inf, None)):
    n = adj_mat.shape[0]
    if v == n:
        if is_solution(cliques, adj_mat):
            if len(set(list(cliques))-set({0})) < best[0]:
                best = (len(set(list(cliques))), cliques_from_list(cliques))

    else:
        for i in range(1, v+2):
            cliques[v] = i
            if is_solution(cliques, adj_mat):
                if len(set(list(cliques))-set({0})) < best[0]:
                    best = backtrack(adj_mat, cliques, v+1, best)
            cliques[v] = 0
    return best


def main():
    # test_graph = load_graph('instance3.clq')
    test_graph = test_graph1
    start_time = time.time()
    cliques = [0 for x in range(test_graph.shape[0])]
    cliques[0] = 1
    solution = backtrack(test_graph, cliques, 1)
    print(solution[0], "cliques:", solution[1])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()