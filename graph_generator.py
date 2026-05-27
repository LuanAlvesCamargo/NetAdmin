import json

import networkx as nx
import matplotlib.pyplot as plt


def load_graph():

    with open("network.json", "r") as file:
        data = json.load(file)

    graph = nx.Graph()

    for node in data["nodes"]:

        graph.add_node(
            node["id"],
            type=node["type"]
        )

    for edge in data["edges"]:

        graph.add_edge(
            edge["source"],
            edge["target"],
            weight=edge["weight"]
        )

    return graph


def draw_graph(graph, shortest_path=None):

    plt.figure(figsize=(14, 9))

    pos = nx.spring_layout(
        graph,
        seed=42
    )

    edge_labels = nx.get_edge_attributes(
        graph,
        "weight"
    )

    node_colors = []

    for node in graph.nodes(data=True):

        node_type = node[1].get("type")

        if node_type == "router":
            node_colors.append("skyblue")

        elif node_type == "server":
            node_colors.append("lightgreen")

        elif node_type == "user":
            node_colors.append("orange")

        else:
            node_colors.append("gray")

    nx.draw(
        graph,
        pos,

        with_labels=True,

        node_color=node_colors,

        node_size=2500,

        font_size=10,

        font_weight="bold"
    )

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels
    )

    if shortest_path:

        path_edges = list(
            zip(
                shortest_path,
                shortest_path[1:]
            )
        )

        nx.draw_networkx_edges(
            graph,
            pos,

            edgelist=path_edges,

            edge_color="red",

            width=4
        )

    plt.title(
        "Topologia da Rede"
    )

    plt.savefig(
        "static/images/graph.png"
    )

    plt.close()