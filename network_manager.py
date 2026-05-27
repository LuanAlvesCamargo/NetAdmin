import json


NETWORK_FILE = "network.json"


class NetworkManager:

    def load_data(self):
        with open(NETWORK_FILE, "r") as file:
            return json.load(file)


    def save_data(self, data):
        with open(NETWORK_FILE, "w") as file:
            json.dump(data, file, indent=4)


    def add_node(self, node_id, node_type):
        data = self.load_data()

        data["nodes"].append({
            "id": node_id,
            "type": node_type
        })

        self.save_data(data)


    def remove_node(self, node_id):
        data = self.load_data()

        data["nodes"] = [
            node for node in data["nodes"]
            if node["id"] != node_id
        ]

        data["edges"] = [
            edge for edge in data["edges"]
            if edge["source"] != node_id
            and edge["target"] != node_id
        ]

        self.save_data(data)