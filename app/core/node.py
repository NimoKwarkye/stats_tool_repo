from abc import ABC, abstractmethod
import os
import pandas as pd
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
    
    def add_input_port(self, name:str, port_type:list[PortType], port_alias="", required=False):
        name = name.replace("_", "")
        if len(port_alias) == 0:
            port_alias = name
        port_index = len(self.input_ports)
        port = Port(name, port_alias, port_type, port_index, self.node_id, 'in', required)
        self.input_ports.append(port)
        return port.port_id


    def add_output_port(self, name:str, port_type:PortType, port_alias=""):
        name = name.replace("_", "")
        if len(port_alias) == 0:
            port_alias = name
        port_index = len(self.output_ports)
        port = Port(name, port_alias, port_type, port_index, self.node_id, 'out')
        self.output_ports.append(port)
        return port.port_id
    
    def save_node_results(self, out_dir:str):
        dir_name, data = self.pre_save()
        if data is not None:
            save_dir = os.path.join(out_dir, dir_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            for key, value in data.items():
                file_name = os.path.join(save_dir, key + ".csv")
                value.to_csv(file_name, index=False)

    
    def get_input_data(self):
        ret_data = {}
        for port in self.input_ports:
            key = port.connection
            if key in port.value:
                ret_data[port.port_id] = port.value[key]

        return ret_data
    
    def get_output_data(self):
        ret_data = {}
        for port in self.output_ports:
            ret_data[port.port_id] = port.value[port.port_id]
        return ret_data
    
    def store_data_in_ports(self, data):
        for port in self.output_ports:
            key = port.port_id
            if key in data and data[key] is not None:
                port.value[key] = data[key]
            else:
                port.value[key] = None

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
    
    def get_port_connection(self, port_id):
        for port in self.input_ports:
            if port.port_id == port_id:
                return port.connection
        raise ValueError(f"Output port '{port_id}' not found in node {self.node_id}.")
    
    def compose_dir_name(self, port_id):
        connected_to = self.get_port_connection(port_id)
        if connected_to is not None:
            split_conn = connected_to.split("_")
            return f"{split_conn[1]}_{split_conn[2]}_{self.node_id}"
        return self.node_id


    @abstractmethod
    def compute(self):
        """Execute the node's operation."""
        pass
    @abstractmethod
    def pre_save(self):
        """Save computed node data."""
        pass

