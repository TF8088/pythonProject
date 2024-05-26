class Node:
    def __init__(self, name, connections=None, value=None):
        self.name = name
        self.connections = connections if connections else {}
        self.value = value


class Graph:
    def __init__(self, graph_dict=None):
        self.nodes = {}
        if graph_dict:
            for node, data in graph_dict.items():
                connections = data.get('connections')
                value = data.get('value')
                self.add_node(Node(node, connections, value))

    def add_node(self, node):
        self.nodes[node.name] = node
        for connection, distance in node.connections.items():
            if connection in self.nodes:
                self.nodes[connection].connections[node.name] = distance

    def get_node(self, name):
        return self.nodes.get(name)

    def update_node(self, name, connections=None, value=None):
        node = self.get_node(name)
        if node:
            if connections:
                node.connections = connections
                for connection, distance in connections.items():
                    if connection in self.nodes:
                        self.nodes[connection].connections[name] = distance
            if value is not None:
                node.value = value

    def update_node_name(self, old_name, new_name):
        node = self.get_node(old_name)
        if node:
            node.name = new_name
            self.nodes[new_name] = self.nodes.pop(old_name)
            for n in self.nodes.values():
                if old_name in n.connections:
                    n.connections[new_name] = n.connections.pop(old_name)

    def delete_node(self, name):
        if name in self.nodes:
            for connection in self.nodes[name].connections:
                if connection in self.nodes:
                    self.nodes[connection].connections.pop(name, None)
            del self.nodes[name]

    def remove_connection(self, name1, name2):
        node1 = self.get_node(name1)
        node2 = self.get_node(name2)
        if node1 and node2:
            node1.connections.pop(name2, None)
            node2.connections.pop(name1, None)
