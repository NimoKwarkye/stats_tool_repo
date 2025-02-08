from app.core.node import Node

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
        self.connections = [con for con in self.connections if node_id not in con]
        self.nodes.pop(node_id)

    def disconnect(self, port_name):
        for con in self.connections:
            if port_name in con:
                self.nodes[con[2]].open_port(port_name)
        self.connections = [con for con in self.connections if port_name not in con]



    def topological_sort(self):
        # For demonstration, we assume nodes can be executed in the order they were added.
        return list(self.nodes.values())

    def execute(self):
        print("GraphManager: Executing graph...")
        for node in self.topological_sort():
            try:
                node.compute()
            except Exception as e:
                print(f"Error computing node {node.node_id}: {e}")