#!/bin/env python


import networkx as nx


def main() -> None:
    with open("input.txt") as f:
        graph = nx.Graph()
        for node_0, node_1 in [l.split("-") for l in f.read().strip().splitlines()]:
            graph.add_edge(node_0, node_1)

        all_inteconnected_nodes = set[tuple[str, str, str]]()
        for node_0 in graph.nodes:
            node_0_contains_t = node_0[0] == "t"
            for node_1 in graph.neighbors(node_0):
                node_1_contains_t = node_1[0] == "t"
                for node_2 in graph.neighbors(node_1):
                    node_2_contains_t = node_2[0] == "t"

                    if not (
                        node_0_contains_t or node_1_contains_t or node_2_contains_t
                    ):
                        continue

                    if node_0 not in graph.neighbors(node_2):
                        continue

                    all_inteconnected_nodes.add(tuple(sorted((node_0, node_1, node_2))))

        print(f"Part 1: {len(all_inteconnected_nodes)}")

        largest_clique = list[str]()
        for clique in nx.find_cliques(graph):
            if len(clique) > len(largest_clique):
                largest_clique = clique

        print(f"Part 2: {",".join(sorted(largest_clique))}")


if __name__ == "__main__":
    main()
