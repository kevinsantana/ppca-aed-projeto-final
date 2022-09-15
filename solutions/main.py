import os
import glob
import _thread
import argparse
import threading
from contextlib import contextmanager

import numpy as np
import pandas as pd
from loguru import logger

from solutions.exact_solution.greedy import greedy_search
from solutions.heuristics.ant_colony_optimization import AntClique, read_graph


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException()
    finally:
        timer.cancel()


def parse_input_args():
    root_parser = argparse.ArgumentParser(add_help=False)

    root_parser.add_argument(
        "--input-dir",
        dest="input_dir",
        help="Run the program on all files inside dimacs_benchmark_set",
    )

    root_parser.add_argument(
        "-i",
        "--input-path",
        dest="input_path",
        help="Input path for single file",
        default=os.path.join(
            "../dimacs_benchmark_set/abhik1505040_max_clique_implementations",
            "anna.col",
        ),
    )

    root_parser.add_argument(
        "-o",
        "--output-prefix",
        dest="output_prefix",
        help="Output path for reports.",
        default="../results",
    )

    root_parser.add_argument(
        "--time-limit",
        dest="time_limit",
        help="time limit for each graph run(s) in seconds.",
        type=int,
        default=1200,
    )

    parser = argparse.ArgumentParser(description="run")
    subparsers = parser.add_subparsers(dest="method", help="Available methods")
    subparsers.required = True

    # options for ant-clique
    parser_aco = subparsers.add_parser(
        "aco", help="Use ant-clique algorithm", parents=[root_parser]
    )
    parser_aco.add_argument(
        "--ants", dest="num_ants", help="num_ants", type=int, default=7
    )
    parser_aco.add_argument(
        "--taomin", dest="taomin", help="taomin", type=float, default=0.01
    )
    parser_aco.add_argument(
        "--taomax", dest="taomax", help="taomax", type=float, default=4
    )
    parser_aco.add_argument(
        "--alpha", dest="alpha", help="alpha", type=float, default=2
    )
    parser_aco.add_argument("--rho", dest="rho", help="rho", type=float, default=0.995)
    parser_aco.add_argument(
        "--max_cycles", dest="max_cycles", help="max_cycles", type=int, default=1000
    )
    parser_aco.add_argument(
        "--runs_per_graph",
        dest="runs_per_graph",
        help="runs_per_graph",
        type=int,
        default=3,
    )

    # options for bnb
    parser_bnb = subparsers.add_parser(
        "bnb", help="Use Branch and Bound algorithm", parents=[root_parser]
    )
    parser_bnb.add_argument("--lb", dest="lb", help="lower_bound", type=int, default=0)

    # options for backtracking
    parser_backt = subparsers.add_parser(
        "greedy", help="Use greedy search algorithm", parents=[root_parser]
    )
    parser_backt.add_argument("--graph", dest="graph", help="test_graph")
    parser_backt.add_argument(
        "--runs_per_graph",
        dest="runs_per_graph",
        help="runs_per_graph",
        type=int,
        default=3,
    )

    return parser.parse_args()


def main(args):
    print(args)
    files, results = [], []
    if args.input_dir:
        root_dirs = glob.glob("../dimacs_benchmark_set" + "/*")
        for dir in root_dirs:
            for file in os.listdir(dir):
                files.append(f"{dir}/{file}")
    elif args.input_path:
        files = [args.input_path]

    output_path = f"{args.output_prefix}/{args.method}_{len(files)}_graphs.csv"

    if args.method == "aco":
        obj = AntClique(
            args.num_ants,
            args.taomin,
            args.taomax,
            args.alpha,
            args.rho,
            args.max_cycles,
        )

        for f in files:
            graph = read_graph(f)
            outputs = []
            for i in range(args.runs_per_graph):
                logger.info(f"Run {i}")
                try:
                    with time_limit(args.time_limit):
                        outputs.append(obj.run(graph))
                except TimeoutException:
                    logger.info("Execution timed out!")
                    continue

            sizes = [o[0] for o in outputs]
            times = [o[1] for o in outputs]
            cycles = [o[2] for o in outputs]

            out_json = {
                "filename": [f],
                "size->mean(stdev)": [f"{np.mean(sizes):.4f}({np.std(sizes):.4f})"],
                "time->mean(stdev)": [f"{np.mean(times):.4f}({np.std(times):.4f})"],
                "cycles->mean(stdev)": [f"{np.mean(cycles):.4f}({np.std(cycles):.4f})"],
            }
            log_msg = "Final results-> " + ", ".join(
                f"{k}: {v[0]}" for k, v in out_json.items()
            )

            results.append(pd.DataFrame(out_json))
            logger.info(log_msg)
            print("\n")

    elif args.method == "greedy":
        for f in files:
            graph = read_graph(f)
            cliques = [0 for x in range(graph.shape[0])]
            cliques[0] = 1
            outputs = []
            for i in range(args.runs_per_graph):
                logger.info(f"Run {i}")
                try:
                    with time_limit(args.time_limit):
                        solution = greedy_search(graph, cliques, 1)
                        outputs.append(solution)
                except TimeoutException:
                    logger.info("Execution timed out!")
                    continue

            sizes = [o[0] for o in outputs]
            cycles = [o[1] for o in outputs]

            out_json = {
                "filename": [f],
                "size->mean(stdev)": [f"{np.mean(sizes):.4f}({np.std(sizes):.4f})"],
                "cycles->mean(stdev)": [f"{np.mean(cycles):.4f}({np.std(cycles):.4f})"],
            }
            log_msg = "Final results-> " + ", ".join(
                f"{k}: {v[0]}" for k, v in out_json.items()
            )

            results.append(pd.DataFrame(out_json))
            logger.info(log_msg)
            print("\n")

    combined_results = pd.concat(results)
    combined_results.to_csv(output_path, index=False)


if __name__ == "__main__":
    args = parse_input_args()
    main(args)
