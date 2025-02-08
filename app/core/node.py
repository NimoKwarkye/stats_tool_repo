from abc import ABC, abstractmethod

from app.core.port import Port


class Node(ABC):
    def __init__(self, node_id, name):
        self.node_id = node_id
        self.name : str = name
        self.input_ports : list[Port] = []    # Mapping from input port name to value.
        self.output_ports : list[Port] = []   # Mapping from output port name to computed value.
        self.params = {}    # Configuration parameters for the node.
        self.position = []
        self.node_index = 0

    
    def add_input_port(self, name, port_type):
        port = Port(name, port_type, 'in')
        self.input_ports.append(port)


    def add_output_port(self, name, port_type):
        port = Port(name, port_type, 'out')
        self.output_ports.append(port)
    
    
    def set_input(self, port_name, value):
        for port in self.input_ports:
            if port.name == port_name:
                port.value = value
                return
        raise ValueError(f"Input port '{port_name}' not found in node {self.node_id}.")


    def get_output(self, port, port_name):
        for port in self.output_ports:
            if port.name == port_name:
                return port.value
        raise ValueError(f"Output port '{port_name}' not found in node {self.node_id}.")

    def close_port(self, port_name):
        for idx, port in enumerate(self.input_ports):
            if port.name == port_name:
                self.input_ports[idx].port_open = False
    
    def open_port(self, port_name):
        for idx, port in enumerate(self.input_ports):
            if port.name == port_name:
                self.input_ports[idx].port_open = True
                print("opened port ", port_name)


    @abstractmethod
    def compute(self):
        """Execute the node's operation."""
        pass

