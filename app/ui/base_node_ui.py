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
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.port_id,
                                    attribute_type=dpg.mvNode_Attr_Input,
                                    user_data=[self.node_id, att.port_id]):
                    dpg.add_text(att.alias)
            
            for idx, att in enumerate(self.node_instance.output_ports):
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.port_id,
                                    attribute_type=dpg.mvNode_Attr_Output,
                                    user_data=[self.node_id, att.port_id]):
                    dpg.add_text(att.alias)

    def node_popup(self):
        raise NotImplementedError 

    def set_current_pos(self):
        self.node_instance.position = dpg.get_item_pos(self.node_id)   
    
    def update_ui(self):
        raise NotImplementedError
    
    def delete_ui(self):
        
        if dpg.does_item_exist(self.node_id):
            dpg.delete_item(self.node_id, children_only=True)
            dpg.delete_item(self.node_id)

        children = dpg.get_item_children(self.parent)
        for child in children:
            for kid in children[child]:
                if self.node_id in dpg.get_item_alias(kid):
                    if dpg.does_item_exist(kid):
                        dpg.delete_item(kid)
    