import dearpygui.dearpygui as dpg

from app import constants
from app.algorithms import (pca)
from sklearn import datasets
from app.plot import app_graph as gph
import numpy as np
from app.gui import pca_ui


# Padding around the entire content
XPADDING = 35
YPADDING = 60

# Tags for our windows/panels so we can refer to them later.
MAIN_WINDOW_TAG       = "MainWindow"
PLOT_AREA_TAG         = "PlotArea"
FOOTER_TAG            = "Footer"
FUNCTIONS_PANEL_TAG   = "FunctionsPanel"
NODE_EDITOR_PANEL_TAG = "NodeEditorPanel"
NODE_EDITOR_TAG       = "node_editor"
REF_NODE_TAG = "ref_node"
node_count=0
class App_Ui:
    def __init__(self):
        self.primar_window = None
        self.graph = None
        
    
    def __call__(self):
        with dpg.window(tag=MAIN_WINDOW_TAG, 
                    label="Data Visualizer App", 
                    no_close=True, 
                    no_collapse=True,
                    no_scrollbar=True,
                    no_scroll_with_mouse=True,
                    no_title_bar=True
                    ):
        
            # -------------------------
            # Plot Area: Top 70%
            # -------------------------
            with dpg.child_window(tag=PLOT_AREA_TAG, border=False):
                dpg.add_text("Plot Area")
                # Insert your plotting widgets here (e.g., dpg.add_plot, dpg.draw_* functions, etc.)
            
            # -------------------------
            # Footer: Bottom 30%
            # -------------------------
            with dpg.child_window(tag=FOOTER_TAG, border=False):
                # Group for horizontal layout in the footer.
                with dpg.group(horizontal=True):
                    
                    # Pre-defined Functions Panel (Left 30%)
                    with dpg.child_window(tag=FUNCTIONS_PANEL_TAG, border=True):
                        dpg.add_text("Pre-defined Functions")
                        with dpg.group():
                            # Function A drag source.
                            btn_a = dpg.add_button(label="Function A")
                            btn_b = dpg.add_button(label="Function B")
                            with dpg.drag_payload(parent=btn_a, payload_type="function_drag", 
                                                drag_data={"name":"Function A", "value":dpg.mvNode_Attr_Input}):
                                dpg.add_text("Draging Function A")
                            # Function B drag source.
                            with dpg.drag_payload(parent=btn_b, payload_type="function_drag", 
                                                drag_data={"name":"Function B", "value":dpg.mvNode_Attr_Output}):
                                dpg.add_text("Draging Function B")
                    
                    # Node Editor Panel (Right 70%)
                    with dpg.child_window(tag=NODE_EDITOR_PANEL_TAG, border=True, drop_callback=self.drop_callback, 
                                        payload_type="function_drag"):
                        with dpg.node_editor(tag=NODE_EDITOR_TAG, 
                                            callback=self.link_callback, delink_callback=self.delink_callback,
                                            minimap=True):
                            # Example node inside the node editor.
                            with dpg.node(label="Example Node"):
                                dpg.add_node_attribute(label="Output", attribute_type=dpg.mvNode_Attr_Output)
                                dpg.add_node_attribute(label="Input", attribute_type=dpg.mvNode_Attr_Input)
                            with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                                # No attributes needed.
                                pass
                            #dpg.add_drag_payload(payload_type="function_drag", callback=drop_callback, parent=NODE_EDITOR_PANEL_TAG)
    

    def drop_callback(self, sender, app_data, user_data):
        """
        Called when a function drag payload is dropped on the node editor area.
        Creates a new node based on the function payload.
        """
        global node_count
        # app_data is the payload sent by the drag source.
        function_name = app_data["name"]  
        node_count += 1
        new_node_label = f"{function_name} Node {node_count}"
        global_mouse_pos = dpg.get_mouse_pos(local=False)
        
        # Force the reference node to render so its rect is updated.
        # If the reference node is hidden, temporarily show it.
        dpg.show_item(REF_NODE_TAG)
        dpg.split_frame()  # Wait one frame so that its rect is computed.
        
        # Get the reference node's screen (rect) and grid positions.
        ref_rect_min = dpg.get_item_rect_min(REF_NODE_TAG)
        ref_grid_pos = dpg.get_item_pos(REF_NODE_TAG)
        
        # Hide the reference node again if you want it invisible.
        dpg.hide_item(REF_NODE_TAG)
        
        # Compute the drop position in node editor coordinates.
        # Essentially, find the difference between the mouse and the ref node’s screen position,
        # then add the ref node's known grid position.
        local_x = global_mouse_pos[0] - ref_rect_min[0] + ref_grid_pos[0]
        local_y = global_mouse_pos[1] - ref_rect_min[1] + ref_grid_pos[1]
        # Create a new node in the node editor.
        with dpg.node(label=new_node_label, parent=NODE_EDITOR_TAG, pos=(local_x, local_y)):
            with dpg.node_attribute(label=f"Output_{node_count}", attribute_type=app_data["value"]):
                dpg.add_text("Node text")
        print(f"Created new node: {new_node_label}")

    def resize_callback(self, sender, app_data):
        # app_data returns a tuple (width, height)
        viewport_width, viewport_height, *_ = app_data

        # Compute the available content size after accounting for padding.
        content_width  = viewport_width 
        content_height = viewport_height

        # Calculate dimensions for each section
        plot_area_height   = int(content_height * 0.70)
        footer_height      = content_height - plot_area_height - YPADDING

        functions_panel_width = int(content_width * 0.30)
        node_editor_width     = content_width - functions_panel_width - XPADDING

        # Reconfigure the main window to occupy the content area with the specified padding.
        dpg.configure_item(MAIN_WINDOW_TAG, width=content_width, height=content_height)
        dpg.set_item_pos(MAIN_WINDOW_TAG, [0, 0])

        # Reconfigure the Plot Area
        dpg.configure_item(PLOT_AREA_TAG, width=content_width, height=plot_area_height)

        # Reconfigure the Footer and its sub-windows
        dpg.configure_item(FOOTER_TAG, width=content_width, height=footer_height)
        dpg.configure_item(FUNCTIONS_PANEL_TAG, width=functions_panel_width, height=footer_height)
        dpg.configure_item(NODE_EDITOR_PANEL_TAG, width=node_editor_width, height=footer_height)

    def link_callback(self, sender, app_data):
        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)

    # callback runs when user attempts to disconnect attributes
    def delink_callback(self, sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)

    def pca_callback(self):
        with dpg.window(label="PCA Parameters Window", height=500, width=300):
            pass

    def pca_exe_callback(self, raw_data:np.ndarray, input_data: pca.PCA_Input, targets:list):
        pca_instance = pca.PCA(input_data, raw_data)
        results = pca_instance()
        self.graph.init_plot([list(results[:, 0]), list(results[:, 1]), targets], gph.pca_plotter)
        

    def main_menubar(self):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New")
                dpg.add_menu_item(label="Open")
            
            with dpg.menu(label="Edit"):
                dpg.add_menu_item(label="Something")
                dpg.add_menu_item(label="Preferences")
            
            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="PCA", callback=pca_ui.show)
                dpg.add_menu_item(label="Factor Analysis")
                dpg.add_menu_item(label="Parallel Factor Analysis")
        
    

   


