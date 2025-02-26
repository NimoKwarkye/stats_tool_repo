import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.ui.base_node_ui import BaseNodeUI


class NodeUIManager:
    def __init__(self, node_ui_map: dict[str, BaseNodeUI]):
        self.node_ui_map = node_ui_map
        self.node_ui_registry = {}

    def create_node_ui(self, node_instance: Node):
        node_type = node_instance.__class__.__name__
        node_ui = self.node_ui_map[node_type](node_instance)
        self.node_ui_registry[node_instance.node_id] = node_ui
        self.draw_node_ui(node_instance.node_id)

    def draw_node_ui(self, node_id: str):
        self.node_ui_registry[node_id].draw_node()
    
    def update_node_ui(self, node_id: str):
        if self.node_ui_registry.get(node_id):
            self.node_ui_registry[node_id].update_ui()
    
    def remove_node_ui(self, node_id: str):
        if self.node_ui_registry.get(node_id):
            self.node_ui_registry[node_id].delete_ui()
            del self.node_ui_registry[node_id]
    
    def set_current_pos(self, node_id: str):
        if self.node_ui_registry.get(node_id):
            self.node_ui_registry[node_id].set_current_pos()