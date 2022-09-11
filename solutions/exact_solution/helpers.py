import argparse
from itertools import combinations

import numpy as np


def load_graph(file):
    """
    Loads a graph from a .clq (DIMACS) file
    """
    with open(file) as f:
        lines = [line for line in f.readlines()]
    
    lines = [line.strip().split() for line in lines if line.strip().split() != []]
    p_line = [line for line in lines if line[0] == "p"][0]
    e_lines = [line for line in lines if line[0] == "e"]
    n = int(p_line[2])
    print("Number of vertices:", n)
    print("Number of edges:", len(e_lines))
    adjmat = [[0] * n for _ in range(len(e_lines))]
    
    for e in e_lines:
        v, w = int(e[1]), int(e[2])

        if v == w:
            print("Loop detected"), v

        if adjmat[v][w]:
            print("Duplicate edge"), v, w

        adjmat[v][w] = adjmat[v][w] = 1

    return (np.array(adjmat), n, len(e_lines))


def make_matrix(rows: int, columns: int, entries):
    """
    Creates a adj matrix from user entry
    """
    matrix = np.array(entries).reshape(rows, columns)
    print(repr(matrix))
    return matrix


def triangles(adj_mat):
    edges = all_edges(adj_mat)
    triangles = []

    for edge in edges:
        for neighbor in neighbors(edge[0], adj_mat):
            if is_edge(neighbor, edge[0], adj_mat) and is_edge(
                neighbor, edge[1], adj_mat
            ):
                triangles.append(set([neighbor, edge[0], edge[1]]))

    return triangles


def neighbors(nodes, adj_mat):
    """
    Takes one or a list of nodes (each one between 1 and N) and returns its neighbors (between 1 and N)
    """

    neighbors = set()
    if isinstance(nodes, int):
        nodes = [nodes]

    for node in nodes:
        if node == 0:
            raise Exception("Node can't be 0: nodes are between 1 and N")

        for i in range(adj_mat.shape[0]):
            neighbor = adj_mat[node - 1, i]
            if neighbor and (i != node):
                neighbors.add(i + 1)

    return neighbors


def is_clique(nodes, adj_mat):
    """
    Check if there is a clique between nodes in adj matrix
    """
    for node_i, node_j in combinations(nodes, 2):
        if not is_edge(node_i, node_j, adj_mat):
            return False

    return True


def find_clique_dumb(node, adj_mat):
    """
    Returns one clique to which the vertice "node" belongs
    """

    clique = set([node])
    node_neighbors = set(neighbors(node, adj_mat))
    while node_neighbors:
        neighbor = node_neighbors.pop()
        if is_clique(clique.union(set([neighbor])), adj_mat):
            clique.add(neighbor)
    return clique


def is_edge(u, v, adj_mat):
    """
    Check if is a edge
    """
    return adj_mat[u - 1, v - 1] or adj_mat[v - 1, u - 1]


def all_edges(adj_mat):
    n = adj_mat.shape[0]
    edges = set()
    for i in range(n):
        for j in range(i + 1):
            if adj_mat[i, j]:
                edges.add((i + 1, j + 1))
    return edges


def is_in_clique(v, clique, adj_mat):
    is_in = True
    if clique is None:
        return False
    for node in clique:
        if not is_edge(v, node, adj_mat):
            is_in = False
    return is_in


def is_solution(nodes_list, adj_mat, v=None):
    """
    Verifies if the cliques in x up to v are indeed cliques
    """

    if v is None:
        v = adj_mat.shape[0]

    cliques_dict = cliques_from_list(nodes_list, v)

    for clique_nodes in cliques_dict.values():
        if not is_clique(clique_nodes, adj_mat):
            return False

    return True


def cliques_from_list(nodes_list, v=None):
    """
    Takes the list X = [1 1 2 3 3 ... ] of nodes containing the label of their associated clique, and returns a dict of
    the different cliques
    """

    if v is None:
        v = len(nodes_list)
    cliques = dict()

    for i in range(v):
        clique = nodes_list[i]

        if clique == 0:
            continue

        if clique in list(cliques):
            cliques[clique].add(i + 1)

        else:
            cliques[clique] = set([i + 1])

    return cliques


def main():
    parser = argparse.ArgumentParser(description="Creates a adj matrix")
    parser.add_argument(
        "--rows", type=int, metavar="r", help="number of rows", required=True
    )
    parser.add_argument(
        "--columns", type=int, metavar="c", help="number of columns", required=True
    )
    parser.add_argument(
        "--entries",
        type=int,
        metavar="e",
        help="entries in a single line separated by space",
        required=True,
        nargs="+",
    )
    args = parser.parse_args()
    make_matrix(args.rows, args.columns, args.entries)


if __name__ == "__main__":
    a = load_graph("/media/rebellion/LORDS_BLADE/python/mestrado/aed/ppca-aed-projeto-final/dimacs_benchmark_set/second_dimacs_implementation_challenge/C125.9.clq")
    print(a)
    # main()
