import networkx as nx


def bfs(graph, start):
    return list(nx.bfs_tree(graph, start))


def dfs(graph, start):
    return list(nx.dfs_tree(graph, start))


def dijkstra(graph, source, target):
    path = nx.dijkstra_path(graph, source, target, weight="weight")

    cost = nx.dijkstra_path_length(
        graph,
        source,
        target,
        weight="weight"
    )

    return path, cost