from flask import Flask, render_template, request, redirect, url_for
from graph_generator import load_graph, draw_graph
from algorithms import bfs, dfs, dijkstra
from network_manager import NetworkManager

app = Flask(__name__)
manager = NetworkManager()

def get_graph():
    return load_graph()

@app.route("/")
def index():
    graph = get_graph()
    
    # Executa os algoritmos de busca e roteamento
    bfs_result = bfs(graph, "Core")
    dfs_result = dfs(graph, "Core")
    shortest_path, cost = dijkstra(graph, "Core", "User4")
    
    # Gera a imagem do grafo destacando o caminho mais curto
    draw_graph(graph, shortest_path)
    
    return render_template(
        "index.html",
        bfs_result=bfs_result,
        dfs_result=dfs_result,
        shortest_path=shortest_path,
        cost=cost
    )

@app.route("/topology")
def topology():
    graph = get_graph()
    draw_graph(graph)
    return render_template("topology.html")

@app.route("/manage")
def manage_network():
    data = manager.load_data()
    return render_template("manage_network.html", data=data)

@app.route("/add-user", methods=["POST"])
def add_user():
    user_id = request.form["user_id"]
    router_id = request.form["router_id"]
    
    manager.add_node(user_id, "user")
    manager.add_edge(router_id, user_id, 1)
    
    return redirect(url_for("manage_network"))

@app.route("/remove-user", methods=["POST"])
def remove_user():
    user_id = request.form["user_id"]
    manager.remove_node(user_id)
    return redirect(url_for("manage_network"))

@app.route("/add-node", methods=["POST"])
def add_node():
    node_id = request.form["node_id"]
    node_type = request.form["node_type"]
    
    manager.add_node(node_id, node_type)
    return redirect(url_for("manage_network"))

@app.route("/remove-node", methods=["POST"])
def remove_node():
    node_id = request.form["node_id"]
    manager.remove_node(node_id)
    return redirect(url_for("manage_network"))

if __name__ == "__main__":
    app.run(debug=True)