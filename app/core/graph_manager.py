from app.core.node import Node, Port
import json
from app.utils.log_handler import LogHandler
import warnings
import uuid
class GraphManager:
    def __init__(self):
        self.nodes = {}         # Map node_id to node instance.
        self.connections = []   # List of connections:
        self.logs_handler: LogHandler = LogHandler() # Each connection is (source_id, source_port, target_id, target_port).
        self.warning_message = None
        warnings.showwarning = self.warning_logs

    def add_node(self, node:Node):
        self.nodes[node.node_id] = node

    def connect(self, source_id, source_port_id, target_id, target_port_id):
        
        if source_id == target_id:
            return False
        
        source_node :Node = self.nodes.get(source_id)
        target_node :Node = self.nodes.get(target_id)

        if not source_node or not target_node:
            self.logs_handler.add_log("GraphManager: One of the nodes not found.", -1)
            return False
        source_port = next((p for p in source_node.output_ports if p.port_id == source_port_id), None)
        target_port = next((p for p in target_node.input_ports if p.port_id == target_port_id), None)
        
        if target_port is None:
            target_port = next((p for p in target_node.output_ports if p.port_id == target_port_id), None)
        if source_port is None:
            source_port = next((p for p in source_node.input_ports if p.port_id == source_port_id), None)

        if source_port is None or target_port is None:
            return False
        
        if target_port.direction == source_port.direction:
            return False
        
        if target_port.direction == "out":
            
            temp_port = target_port
            target_port = source_port
            source_port = temp_port

            temp_node = target_node
            target_node = source_node
            source_node = temp_node
        
        if source_port.port_type not in target_port.port_type:
            return False
        
        if not target_port.port_open:
            return False
        
        self.connections.append((source_node.node_id, source_port.port_id, target_node.node_id, target_port.port_id))
        target_port.connection = source_port.port_id
        target_node.set_input(target_port.port_id, source_port.value)
        target_node.close_port(target_port.port_id)
        return True

    def remove_node(self, node_id):
        for con in self.connections:
            if node_id in con:
                self.nodes[con[2]].open_port(con[3])
        self.connections = [con for con in self.connections if not node_id  in con]
        self.nodes.pop(node_id)

    def disconnect(self, source_port_id, target_port_id):
        for con in self.connections:
            if source_port_id in con and target_port_id in con:
                self.nodes[con[2]].open_port(target_port_id)
        self.connections = [con for con in self.connections if not (source_port_id in con and target_port_id in con)]
        
    def warning_logs(self, message, category, filename, lineno, file=None, line=None):
        self.warning_message = f"{message}"

    def get_node(self, node_id):
        return self.nodes.get(node_id)
    
    def save_to_file(self, filename, node_factory):
        """
        Serializes the nodes and connections into a JSON file.
        """
        data = {
            'nodes': [],
            'connections': self.connections,
            "node_factory":node_factory.prototypes_count
        }
        for node_id, node in self.nodes.items():
            node_data = {
                'node_id': node_id,
                'node_type': node_id.split("_")[0],  # e.g. "CSVImportNode"
                'params': node.params,
                "position":node.position,
                "node_index":node.node_index
            }
            data['nodes'].append(node_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        self.logs_handler.add_log(f"GraphManager: Graph saved to {filename}")


    def load_from_file(self, filename, node_factory):
        """
        Loads nodes and connections from a JSON file and reconstructs the graph.
        The node_factory is used to create node instances from prototypes.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.nodes.clear()
        self.connections = data.get('connections', [])
        node_factory.prototypes_count.update(data.get("node_factory", {}))
        
        for node_data in data.get('nodes', []):
            node_type = node_data.get('node_type')
            node_id = node_data.get('node_id')
            position = node_data.get('position')
            node_index = node_data.get("node_index", 0)
            node: Node = node_factory.create_from_file(node_id, position, node_type, node_index)
            node.params.update(node_data.get('params', {}))
            self.nodes[node_id] = node
        
        for source_id, source_port, target_id, target_port in self.connections:
            source_node = self.nodes[source_id]
            target_node = self.nodes[target_id]
            target_node.set_input(target_port, source_node.get_output(source_port))
            target_node.add_connection(target_port, source_port)
            target_node.close_port(target_port)
        self.logs_handler.add_log(f"GraphManager: Graph loaded from {filename}")

    def execute(self):
        """
        Executes only the nodes that are part of a connected subgraph.
        Execution is done in topological order.
        """
        if  len(self.connections) == 0:
            self.logs_handler.add_log("GraphManager: No connections found.", 1)
            return False

        incoming_count = {node_id: 0 for node_id in self.nodes}
        for source_id, _, target_id, _ in self.connections:
            incoming_count[target_id] += 1

        queue  = [node for node in self.nodes.values()
                 if incoming_count[node.node_id] == 0 and any(node.node_id in conn for conn in self.connections)]
        if not queue:
            queue = [node for node in self.nodes.values()  for conn in self.connections if node.node_id == conn[0]]
        
        sorted_nodes = []
        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for source_id, _, target_id, _ in self.connections:
                if source_id == node.node_id:
                    incoming_count[target_id] -= 1
                    if incoming_count[target_id] == 0:
                        queue.append(self.nodes[target_id])
        
        for node in sorted_nodes:
            self.warning_message = None
            try:
                node_log = node.compute()
                if self.warning_message:
                    self.logs_handler.add_log(f"{node.node_id}: {self.warning_message}", 1)
                if node_log:
                    self.logs_handler.add_log(f"Computed {node.node_id}\n{node_log}")
            except Exception as e:
                self.logs_handler.add_log(f"Error executing node {node.node_id}\nmsg: {e}", -1)
                return False
        return True