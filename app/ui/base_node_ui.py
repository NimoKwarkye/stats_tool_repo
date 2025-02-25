import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.utils.constants import NODE_EDITOR_TAG

class BaseNodeUI:
    def __init__(self, node_instance:Node):
        self.node_instance = node_instance
        self.node_id = node_instance.node_id
        self.parent = NODE_EDITOR_TAG

    def draw_node(self):
        with dpg.node(label=f"{self.node_instance.name} {self.node_instance.node_index}", 
                        tag=self.node_id, 
                        parent=self.parent, 
                        pos=self.node_instance.position,
                        user_data=[self.node_instance.node_id, 
                                   self.node_instance.__class__.__name__],):
            self.node_popup()
            for idx, att in enumerate(self.node_instance.input_ports):
                self.node_instance.input_ports[idx].port_index = idx
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.name + self.node_id + f"input_{idx}",
                                    attribute_type=dpg.mvNode_Attr_Input,
                                    user_data=[self.node_id, att.name]):
                    dpg.add_text(att.alias)
            
            for idx, att in enumerate(self.node_instance.output_ports):
                self.node_instance.output_ports[idx].port_index = idx
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.name + self.node_id + f"output_{idx}",
                                    attribute_type=dpg.mvNode_Attr_Output,
                                    user_data=[self.node_id, att.name]):
                    dpg.add_text(att.alias)

    def node_popup(self):
        raise NotImplementedError    
    
    def update_ui(self):
        raise NotImplementedError
    
    def delete_ui(self):
        dpg.delete_item(self.node_id)
    
    