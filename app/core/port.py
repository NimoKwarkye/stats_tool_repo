import enum
from typing import Union


class PortType(enum.Enum):
    DATAFRAMEFLOAT = enum.auto()
    DATASERIESFLOAT = enum.auto()
    FEATURELABELSSTRING = enum.auto()
    TARGETLABELSSTRING = enum.auto()
    MODELSERIESFLOAT = enum.auto()
    MODELDATAFRAMEFLOAT = enum.auto()
    MODELOBJECT = enum.auto()

class Port:
    def __init__(self, name:str, port_alias:str, 
                 port_type:Union[PortType, list[PortType]], port_index:int, 
                 node_id:str, direction:str, required:bool=False):
        self.name = name
        self.alias = port_alias            # e.g. "data", "labels", "model"
        self.port_type : Union[PortType, list[PortType]] = port_type  # e.g. "DataFrame", "Series", "Model"
        self.direction = direction  # "in" or "out"
        self.value = {}
        self.port_open = True
        self.port_index = port_index
        self.node_id = node_id
        self.port_id = f"{name}_{node_id}_{direction}put_{port_index}"
        self.connection = None
        self.required = required
    
    

    
    def __repr__(self):
        return f"<Port {self.direction} '{self.name}' ({self.port_id})>"

