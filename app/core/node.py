from abc import ABC, abstractmethod

from app.core.port import Port, PortType


class Node(ABC):
    def __init__(self, node_index, name):
        self.node_id = self.__class__.__name__ + "_" + str(node_index)
        self.name : str = name
        self.input_ports : list[Port] = []    # Mapping from input port name to value.
        self.output_ports : list[Port] = []   # Mapping from output port name to computed value.
        self.params = {}    # Configuration parameters for the node.
        self.position = []
        self.node_index = node_index


    def clone(self, node_index):
        new_node = self.__class__(node_index, self.name)
        return new_node
    
    def add_input_port(self, name:str, port_type:PortType, port_alias=""):
        if len(port_alias) == 0:
            port_alias = name
        port_index = len(self.input_ports)
        port = Port(name, port_alias, port_type, port_index, self.node_id, 'in')
        self.input_ports.append(port)
        return port.port_id


    def add_output_port(self, name:str, port_type:PortType, port_alias=""):
        if len(port_alias) == 0:
            port_alias = name
        port_index = len(self.output_ports)
        port = Port(name, port_alias, port_type, port_index, self.node_id, 'out')
        self.output_ports.append(port)
        return port.port_id
    
    
    def set_input(self, port_id, value):
        for port in self.input_ports:
            if port.port_id == port_id:
                port.value = value
                return
        raise ValueError(f"Input port '{port_id}' not found in node {self.node_id}.")

    def get_input_port_index(self, port_id):
        for idx, port in enumerate(self.input_ports):
            if port.port_id == port_id:
                return port.port_index
        raise ValueError(f"Input port '{port_id}' not found in node {self.node_id}.")
    
    def get_output_port_index(self, port_id):
        for idx, port in enumerate(self.output_ports):
            if port.port_id == port_id:
                return port.port_index
        raise ValueError(f"Output port '{port_id}' not found in node {self.node_id}.")

    def get_output(self, port_id):
        for port in self.output_ports:
            if port.port_id == port_id:
                return port.value
        raise ValueError(f"Output port '{port_id}' not found in node {self.node_id}.")

    def close_port(self, port_id):
        for idx, port in enumerate(self.input_ports):
            if port.port_id == port_id:
                self.input_ports[idx].port_open = False
    
    def open_port(self, port_id):
        for idx, port in enumerate(self.input_ports):
            if port.port_id == port_id:
                self.input_ports[idx].port_open = True
                return
        raise ValueError(f"Input port '{port_id}' not found in node {self.node_id}.")

    def add_connection(self, port_id, source_port_id):
        for idx, port in enumerate(self.input_ports):
            if port.port_id == port_id:
                self.input_ports[idx].connection = source_port_id
                return
        raise ValueError(f"Output port '{port_id}' not found in node {self.node_id}.")
    
    def remove_connection(self, port_id):
        for idx, port in enumerate(self.input_ports):
            if port.port_id == port_id:
                self.input_ports[idx].connection = None
                return
        raise ValueError(f"Output port '{port_id}' not found in node {self.node_id}.")


    @abstractmethod
    def compute(self):
        """Execute the node's operation."""
        pass

