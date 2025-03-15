import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.utils.constants import NODE_EDITOR_TAG

class BaseNodeUI:
    def __init__(self, node_instance:Node):
        self.node_instance = node_instance
        self.node_id = node_instance.node_id
        self.parent = NODE_EDITOR_TAG
        self.required_open_theme = {}
        self.required_closed_theme = {}
        for port in self.node_instance.input_ports:
            if port.required:
                port_open_theme = f"{self.node_id}_{port.port_id}_open_theme"
                port_closed_theme = f"{self.node_id}_{port.port_id}_closed_theme"
                self.create_required_theme((190, 49, 68, 255), port_open_theme)
                self.create_required_theme((93, 255, 54, 255), port_closed_theme)
                self.required_open_theme[port.port_id] = port_open_theme
                self.required_closed_theme[port.port_id] = port_closed_theme


    def draw_node(self):
        with dpg.node(label=f"{self.node_instance.name} {self.node_instance.node_index}", 
                        tag=self.node_id, 
                        parent=self.parent, 
                        pos=self.node_instance.position,
                        user_data=[self.node_instance.node_id, 
                                   self.node_instance.__class__.__name__],):
            self.node_popup()
            for idx, att in enumerate(self.node_instance.input_ports):
                shape = dpg.mvNode_PinShape_TriangleFilled if att.required \
                    else dpg.mvNode_PinShape_CircleFilled
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.port_id,
                                    shape=shape,
                                    attribute_type=dpg.mvNode_Attr_Input,
                                    user_data=[self.node_id, att.port_id]):
                    dpg.add_text(att.alias)
                if att.required:
                    dpg.bind_item_theme(att.port_id, self.required_open_theme[att.port_id])
            
            for idx, att in enumerate(self.node_instance.output_ports):
                with dpg.node_attribute(label=att.name,
                                    parent=self.node_id,
                                    tag = att.port_id,
                                    attribute_type=dpg.mvNode_Attr_Output,
                                    user_data=[self.node_id, att.port_id]):
                    dpg.add_text(att.alias)

    def create_required_theme(self, color, tag):
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvNode_Attr_Input):
                dpg.add_theme_color(dpg.mvNodeCol_Pin, color, 
                                    category=dpg.mvThemeCat_Nodes)
    
        return dpg.get_value("theme")

    def node_popup(self):
        raise NotImplementedError 

    def set_current_pos(self):
        self.node_instance.position = dpg.get_item_pos(self.node_id)   
    
    def update_ui(self):
        raise NotImplementedError
    
    def show_connected(self, port_id):
        for port in self.node_instance.input_ports:
            if port.port_id == port_id and port.required:
                dpg.bind_item_theme(port_id, self.required_closed_theme[port_id])
    
    def show_disconnected(self, port_id):
        for port in self.node_instance.input_ports:
            if port.port_id == port_id and port.required:
                dpg.bind_item_theme(port_id, self.required_open_theme[port_id])

    def delete_ui(self):
        
        if dpg.does_item_exist(self.node_id):
            dpg.delete_item(self.node_id, children_only=True)
            dpg.delete_item(self.node_id)
        
        for port_theme in self.required_open_theme:
            if dpg.does_item_exist(self.required_open_theme[port_theme]):
                dpg.delete_item(self.required_open_theme[port_theme])
        
        for port_theme in self.required_closed_theme:
            if dpg.does_item_exist(self.required_closed_theme[port_theme]):
                dpg.delete_item(self.required_closed_theme[port_theme])

        children = dpg.get_item_children(self.parent)
        for child in children:
            for kid in children[child]:
                if self.node_id in dpg.get_item_alias(kid):
                    if dpg.does_item_exist(kid):
                        dpg.delete_item(kid)
    