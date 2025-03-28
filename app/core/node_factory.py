import copy
from app.core.node import Node
class NodeFactory:
    def __init__(self):
        self.prototypes: dict[str, Node] = {}  # Map from node type name to a prototype instance.
        self.prototypes_count = {}

    def register_prototype(self, type_name, prototype_node):
        self.prototypes[type_name] = prototype_node
        self.prototypes_count[type_name] = {
            "count": 1,
            "old_types": []
        }
        #print(f"NodeFactory: Registered prototype for {type_name}")


    def create_from_file(self, node_id, position, type_name, node_index):
        if type_name not in self.prototypes:
            raise ValueError(f"NodeFactory: Prototype '{type_name}' not registered.")
        # Use deepcopy to clone the prototype.
        new_node : Node = self.prototypes[type_name].clone(node_index)
        new_node.position = position
        
        return new_node


    def create_node(self, type_name, position)->Node:
        if type_name not in self.prototypes:
            raise ValueError(f"NodeFactory: Prototype '{type_name}' not registered.")
        # Use deepcopy to clone the prototype.
        new_index = None
        if len(self.prototypes_count[type_name]["old_types"]) > 0:
            new_index = self.prototypes_count[type_name]["old_types"].pop(0)
        else:
            new_index = self.prototypes_count[type_name]["count"]
            self.prototypes_count[type_name]["count"] += 1
        
        new_node : Node = self.prototypes[type_name].clone(new_index)
        new_node.position = position
        
        return new_node

    def delete_node(self, type_name, node_index):
        if type_name not in self.prototypes:
            raise ValueError(f"NodeFactory: Prototype '{type_name}' not registered.")
        self.prototypes_count[type_name]["old_types"].append(node_index)
        self.prototypes_count[type_name]["old_types"].sort()

        #print(f"NodeFactory: Deleted node {type_name}")