import dearpygui.dearpygui as dpg

from app import constants
from app.algorithms import (pca)
from sklearn import datasets
from app.plot import app_graph as gph
import numpy as np
from app.gui import pca_ui
from enum import Enum, auto


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

class NodeFunction(Enum):
    DATAIMPORT = auto()

class DataLoader():
    instance = None
    def __init__(self, parent:str):
        self.instance_count : int = 1
        self.parent = parent
        self.name = "Data Loader"
    

    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super().__new__(self)
        return self.instance
    
    def generate(self, pos: tuple[int]):
        with dpg.node(label=f"{self.name} {self.instance_count}", parent=self.parent, pos=pos):
            with dpg.node_attribute(label=f"Feature Data##_{node_count}", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_text("Feature Data")
            with dpg.node_attribute(label=f"Feature Labels##_{node_count}", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_text("Feature Names")
            with dpg.node_attribute(label=f"Target Data##_{node_count}", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_text("Target Data")
        self.instance_count +=1


class App_Ui:
    def __init__(self):
        self.primar_window = None
        self.graph = None
        self.data_loader = DataLoader(NODE_EDITOR_TAG)
    
    def __call__(self):
       
        with dpg.window(tag=PLOT_AREA_TAG, 
                        label="Plots", 
                        no_close=True, 
                        no_collapse=True,
                        no_scrollbar=True,
                        no_scroll_with_mouse=True):
            dpg.add_text("Plot Area")
        
        # -------------------------
        # Footer: Bottom 30%
        # -------------------------
        with dpg.window(tag=FOOTER_TAG, 
                        label="Editor", 
                        no_close=True, 
                        no_collapse=True, 
                        no_scrollbar=True,
                        no_scroll_with_mouse=True):
            with dpg.table(header_row=False, borders_innerV=True, resizable=True):
                dpg.add_table_column(width=300)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(tag=FUNCTIONS_PANEL_TAG, border=False):
                        with dpg.group():
                            btn_a = dpg.add_button(label="Data Loader")
                            btn_b = dpg.add_button(label="Function B")
                            with dpg.drag_payload(parent=btn_a, 
                                                drag_data={"name":"Data Loader", "value":NodeFunction.DATAIMPORT}):
                                dpg.add_text("New Data Loader")
                            '''with dpg.drag_payload(
                                                    parent=btn_b, 
                                                    drag_data={"name":"Function B", "value":dpg.mvNode_Attr_Output}):
                                dpg.add_text("Draging Function B")'''
                    
                    with dpg.child_window(
                                            tag=NODE_EDITOR_PANEL_TAG, 
                                            border=False, 
                                            drop_callback=self.drop_callback,
                                            no_scrollbar=True,
                                            no_scroll_with_mouse=True):
                        with dpg.node_editor(tag=NODE_EDITOR_TAG, 
                                            callback=self.link_callback, 
                                            delink_callback=self.delink_callback,
                                            minimap=True):
                            with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                                pass
    

    def drop_callback(self, sender, app_data, user_data):
        """
        Called when a function drag payload is dropped on the node editor area.
        Creates a new node based on the function payload.
        """
        global node_count
        function_name = app_data["name"]  
        node_count += 1
        global_mouse_pos = dpg.get_mouse_pos(local=False)
        
        dpg.show_item(REF_NODE_TAG)
        dpg.split_frame()  
        
        ref_rect_min = dpg.get_item_rect_min(REF_NODE_TAG)
        ref_grid_pos = dpg.get_item_pos(REF_NODE_TAG)
        
        dpg.hide_item(REF_NODE_TAG)
        
        local_x = global_mouse_pos[0] - ref_rect_min[0] + ref_grid_pos[0]
        local_y = global_mouse_pos[1] - ref_rect_min[1] + ref_grid_pos[1]
        match app_data["value"]:
            case NodeFunction.DATAIMPORT:
                self.data_loader.generate((local_x, local_y))
            case _:
                raise ValueError("Invalid node function provided")
        

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
        
    

   


