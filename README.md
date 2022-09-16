# ppca-aed-projeto-final

(PT-BR :brazil:)
Projeto final da disciplina Algoritmos e Estrutura de Dados do Programa de Pós-Graduação em Computação Aplicada (PPCA) da Universidade de Brasília (UnB).

(EN-US :us:)
Final project of Data Structure and Algorithms Class on the Applied Computation Post-Graduation Program of Universidade de Brasília (UnB).

## Graph Format

All graphs are in [DIMACS (ASCII, undirected) format](http://dimacs.rutgers.edu/pub/challenge/graph/doc/ccformat.tex).
For example, a file with the following contents would represent a graph with four
vertices with weights 10, 11, 12, 13 and a single edge from the first vertex
to the second vertex.

    p edge 4 1
    n 1 10
    n 2 11
    n 3 12
    n 4 13
    e 1 2

### Run

1. Install dependencies with

```bash
pip install -e .
```

2. Execute [ppca_aed_projeto_final](ppca_aed_projeto_final), a simple usage can be achieved with

```bash
python ppca_aed_projeto_final aco --input-dir dimacs_benchmark_set
```

Where the first argument `aco` represents the method to find a maximum clique. Avalaible options are:

| Argument    | Method |
| ----------- | ----------------------- |
| aco         | Ant Colony Optimization |
| bnb         | Branch and Bound        |
| greedy      | Greedy Search           |

Second argument `input-dir` where to find the tests graphs.