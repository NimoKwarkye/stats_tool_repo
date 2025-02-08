import copy
from app.core.node import Node
class NodeFactory:
    def __init__(self):
        self.prototypes = {}  # Map from node type name to a prototype instance.

    def register_prototype(self, type_name, prototype_node):
        self.prototypes[type_name] = prototype_node
        print(f"NodeFactory: Registered prototype for {type_name}")

    def create_node(self, type_name, node_id, position)->Node:
        if type_name not in self.prototypes:
            raise ValueError(f"NodeFactory: Prototype '{type_name}' not registered.")
        # Use deepcopy to clone the prototype.
        new_node : Node = copy.deepcopy(self.prototypes[type_name])
        new_node.node_id = node_id
        new_node.position = position
        return new_node