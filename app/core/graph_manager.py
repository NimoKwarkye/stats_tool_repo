from app.core.node import Node
import json

class GraphManager:
    def __init__(self):
        self.nodes = {}         # Map node_id to node instance.
        self.connections = []   # List of connections:
                                # Each connection is (source_id, source_port, target_id, target_port).

    def add_node(self, node:Node):
        self.nodes[node.node_id] = node
        print(f"GraphManager: Added node {node.node_id} ({node.name})")

    def connect(self, source_id, source_port_name, target_id, target_port_name):
        
        if source_id == target_id:
            return False
        
        source_node :Node = self.nodes.get(source_id)
        target_node :Node = self.nodes.get(target_id)

        if not source_node or not target_node:
            raise ValueError("GraphManager: One of the nodes not found.")
        # Locate the output port from the source and the input port from the target.
        source_port = next((p for p in source_node.output_ports if p.name == source_port_name), None)
        target_port = next((p for p in target_node.input_ports if p.name == target_port_name), None)
        
        if target_port is None:
            target_port = next((p for p in target_node.output_ports if p.name == target_port_name), None)
        if source_port is None:
            source_port = next((p for p in source_node.input_ports if p.name == source_port_name), None)

        if source_port is None or target_port is None:
            return False
        
        if target_port.direction == source_port.direction:
            return False
        
        # Enforce type safety.
        if source_port.port_type != target_port.port_type:
            return False
        
        if target_port.direction == "out":
            
            temp_port = target_port
            target_port = source_port
            source_port = temp_port

            temp_node = target_node
            target_node = source_node
            source_node = temp_node
        
        if not target_port.port_open:
            return False
        
        self.connections.append((source_node.node_id, source_port.name, target_node.node_id, target_port.name))
        # Update the target node’s input with the current value of the source’s output.
        target_node.set_input(target_port.name, source_port.value)
        target_node.close_port(target_port.name)
        print(f"GraphManager: Connected {source_node.node_id}.{source_port.name} -> {target_node.node_id}.{target_port.name}")
        return True

    def remove_node(self, node_id):
        for con in self.connections:
            if node_id in con:
                self.nodes[con[2]].open_port(con[3])
        self.connections = [con for con in self.connections if not node_id  in con]
        self.nodes.pop(node_id)

    def disconnect(self, source_port_name, target_port_name):
        for con in self.connections:
            if source_port_name in con and target_port_name in con:
                self.nodes[con[2]].open_port(target_port_name)
        self.connections = [con for con in self.connections if not (source_port_name in con and target_port_name in con)]
        


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
                "input_ports":[[port.name, port.port_type, port.direction, port.port_open, port.port_index] for port in node.input_ports],
                "output_ports":[[port.name, port.port_type, port.direction, port.port_open, port.port_index] for port in node.output_ports],
                "position":node.position,
                "node_index":node.node_index
            }
            data['nodes'].append(node_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"GraphManager: Graph saved to {filename}")

    def load_from_file(self, filename, node_factory):
        """
        Loads nodes and connections from a JSON file and reconstructs the graph.
        The node_factory is used to create node instances from prototypes.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Clear current state
        self.nodes.clear()
        self.connections = data.get('connections', [])
        node_factory.prototypes_count = data.get("node_factory", {})
        
        # Reconstruct nodes
        for node_data in data.get('nodes', []):
            node_type = node_data['node_type']
            node_id = node_data['node_id']
            position = node_data['position']
            # Create a new node instance using the factory.
            node : Node = node_factory.create_from_file(node_id,position, node_type, node_data["node_index"])
            node.params = node_data['params']
            for idx, port_data in enumerate(node_data["input_ports"]):
                node.input_ports[idx].name = port_data[0]
                node.input_ports[idx].port_type = port_data[1]
                node.input_ports[idx].direction = port_data[2]
                node.input_ports[idx].port_open = port_data[3]
                node.input_ports[idx].port_index = port_data[4]
            
            for idx, port_data in enumerate(node_data["output_ports"]):
                node.output_ports[idx].name = port_data[0]
                node.output_ports[idx].port_type = port_data[1]
                node.output_ports[idx].direction = port_data[2]
                node.output_ports[idx].port_open = port_data[3]
                node.output_ports[idx].port_index = port_data[4]

            node_data["input_ports"] = node_data["input_ports"]
            node_data["output_ports"] = node_data["output_ports"]
            self.nodes[node_id] = node
            print(f"GraphManager: Loaded node {node_id} ({node_type})")
        
        # Re-establish connections (and update target node inputs)
        for source_id, source_port, target_id, target_port in self.connections:
            source_node = self.nodes[source_id]
            target_node = self.nodes[target_id]
            target_node.set_input(target_port, source_node.get_output(source_port))
            print(f"GraphManager: Re-connected {source_id}.{source_port} -> {target_id}.{target_port}")
        print(f"GraphManager: Graph loaded from {filename}")

    def execute(self):
        """
        Executes only the nodes that are part of a connected subgraph.
        Execution is done in topological order.
        """
        print("GraphManager: Executing connected nodes...")
        if  len(self.connections) == 0:
            print("GraphManager: No connections found.")
            return False

        # Compute the number of incoming connections for each node.
        incoming_count = {node_id: 0 for node_id in self.nodes}
        for source_id, _, target_id, _ in self.connections:
            incoming_count[target_id] += 1

        # Collect source nodes: those with zero incoming connections and that are connected.
        # (If no such node exists, default to all nodes acting as source connection.)
        queue  = [node for node in self.nodes.values()
                 if incoming_count[node.node_id] == 0 and any(node.node_id in conn for conn in self.connections)]
        if not queue:
            queue = [node for node in self.nodes.values() if node.node_id == conn[0] for conn in self.connections]
        
        # Topologically sort using Kahn's algorithm.
        sorted_nodes = []
        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for source_id, _, target_id, _ in self.connections:
                if source_id == node.node_id:
                    incoming_count[target_id] -= 1
                    if incoming_count[target_id] == 0:
                        queue.append(self.nodes[target_id])
        
        # Execute nodes in sorted order.
        for node in sorted_nodes:
            try:
                node.compute()
            except Exception as e:
                print(f"Error executing node {node.node_id}: {e}")
                return False
        return True