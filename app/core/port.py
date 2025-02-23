import uuid

class Port:
    def __init__(self, name, port_type, direction):
        self.name = name
        self.alias = name            # e.g. "data", "labels", "model"
        self.port_type = port_type  # e.g. "DataFrame", "Series", "Model"
        self.direction = direction  # "in" or "out"
        self.value = []
        self.port_open = True
        self.port_index = 0

    
    def __repr__(self):
        return f"<Port {self.direction} '{self.name}' ({self.port_type})>"

