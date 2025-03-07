import os
import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.core.graph_manager import GraphManager
from app.core.node_factory import NodeFactory
from app.ui.plot_area import PlotArea
from app.ui.ui_manager import NodeUIManager
from app.utils.log_handler import LogHandler 
from app.utils.constants import EDITOR_TAG, FUNCTIONS_PANEL_TAG, NODE_EDITOR_PANEL_TAG, \
                                NODE_EDITOR_TAG, OPENFILE_DIALOG_TAG, REF_NODE_TAG, CSVIMPORT_DRAG_ID, \
                                LINEAR_REG_DRAG_ID, SCATTER_PLOT_DRAG_ID,  LOG_WINDOW_TAG, \
                                SQLDB_IMPORT_DRAG_ID, HEATMAP_PLOT_DRAG_ID, SMP_LINEAR_REG_DRAG_ID, \
                                PCA_DRAG_ID, PAIR_GRID_PLOT_DRAG_ID
from app.utils.node_config import NODE_CONFIG
from collections import defaultdict


NODE_UI_MAPPING = { key: config["ui_class"] for key, config in NODE_CONFIG.items() }
NODE_IDS = { key: f"{config['prototype_id']}{dpg.generate_uuid()}" for key, config in NODE_CONFIG.items() }
NODE_CLASS = { key: config["node_class"] for key, config in NODE_CONFIG.items() }

nodes_by_category = defaultdict(list)
for node_name, config in NODE_CONFIG.items():
    nodes_by_category[config["category"]].append(config)

ui_manager = NodeUIManager(NODE_UI_MAPPING)
graph_manager = GraphManager()
node_factory = NodeFactory()
logs_handler: LogHandler = LogHandler()

plot_area : PlotArea = PlotArea()

for key in NODE_CLASS:
    node_factory.register_prototype(key, NODE_CLASS[key](NODE_IDS[key]))

def execute_graph():
    if graph_manager.execute():
        for node_id in graph_manager.nodes.keys():
            node:Node = graph_manager.get_node(node_id)
            if node.__class__.__name__ == SCATTER_PLOT_DRAG_ID:
                if node.has_data:
                    plot_area.plot_manager.plot(node.params, node.plot_data)
            elif node.__class__.__name__ == HEATMAP_PLOT_DRAG_ID:
                if node.has_data:
                    plot_area.plot_manager.plot(node.params, node.plot_data)
            elif node.__class__.__name__ == PAIR_GRID_PLOT_DRAG_ID:
                if node.has_data:
                    plot_area.plot_manager.plot(node.params, node.plot_data)
            elif node.__class__.__name__ == LINEAR_REG_DRAG_ID:
                ui_manager.update_node_ui(node_id)
        logs_handler.add_log("Graph executed successfully.")
        

def get_relative_mouse_pos(ref_object:str):
    global_mouse_pos = dpg.get_mouse_pos(local=False)
        
    dpg.show_item(ref_object)
    dpg.split_frame()  
    ref_rect_min = dpg.get_item_rect_min(ref_object)
    ref_grid_pos = dpg.get_item_pos(ref_object)
    dpg.hide_item(ref_object)
    local_x = global_mouse_pos[0] - ref_rect_min[0] + ref_grid_pos[0]
    local_y = global_mouse_pos[1] - ref_rect_min[1] + ref_grid_pos[1]
    return [local_x, local_y]


def open_csvfile_dialog_callback(sender, app_data, user_data):
    input_text_tag = user_data
    selected_file = list(app_data['selections'].items())[0][1]
    if dpg.does_item_exist(input_text_tag):
        dpg.set_value(input_text_tag, selected_file)

def save_jsonfile_dialog_callback(sender, app_data, user_data):
    selected_file = app_data["file_path_name"].split(".")[0] + ".json"
    if len(selected_file) == 0:
        return
    for node_id in graph_manager.nodes.keys():
        ui_manager.set_current_pos(node_id)
    graph_manager.save_to_file(selected_file, node_factory)
    logs_handler.add_log("Graph saved successfully.")

def open_jsonfile_dialog_callback(sender, app_data, user_data):
    selected_file = None
    if app_data["selections"].__len__() > 0:
        selected_file = list(app_data['selections'].items())[0][1]
    else:
        selected_file = app_data["file_path_name"]
    if os.path.exists(selected_file):
        node_ids = [ky for ky in graph_manager.nodes.keys()]
        print(node_ids)
        for node_id in node_ids:
            node = graph_manager.get_node(node_id)
            delete_node(node.node_id, node.node_index)
        graph_manager.load_from_file(selected_file, node_factory)
        create_loaded_nodes()
        logs_handler.add_log("Graph loaded successfully.")
    else:
        logs_handler.add_log(f"File: {selected_file} not found.", -1)

def open_file_dialog(tag:str, user_data:str, callback, label="Open File"):
    with dpg.file_dialog(
                         label=label, directory_selector=False, show=False, 
                         tag=f"{OPENFILE_DIALOG_TAG}_{tag}", width=520 ,
                         height=400, modal=True, user_data=user_data,
                         callback=callback):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.csv){.csv}", color=(0, 255, 255, 255))
        dpg.add_file_extension(".csv", color=(255, 0, 255, 255), custom_text="[CSV]")
        dpg.add_file_extension(".json", color=(255, 255, 55, 255), custom_text="[JSON]")


def add_node_callback(sender, app_data, user_data):

    pos = get_relative_mouse_pos(REF_NODE_TAG)
    node = node_factory.create_node(app_data, pos)
    graph_manager.add_node(node)
    ui_manager.create_node_ui(node)


def create_loaded_nodes():
    for node_id, node in graph_manager.nodes.items():
        ui_manager.create_node_ui(node)
        ui_manager.update_node_ui(node_id)
    
    for conn in graph_manager.connections:
        reconnect_loaded_nodes(conn[0], conn[2], conn[1], conn[3])


def reconnect_loaded_nodes(node_1, node_2, port_1, port_2):
    attr_1 = port_1 
    attr_2 = port_2
    tag = f"{node_1}_{node_2}_{attr_1}_{attr_2}" 
    dpg.add_node_link(attr_1, attr_2, parent=NODE_EDITOR_TAG, user_data=[port_1, port_2], tag=tag)

def delink_callback(sender, app_data, user_data):
        # app_data -> link_id
    ports = dpg.get_item_user_data(app_data)
    graph_manager.disconnect(ports[0], ports[1])
    if dpg.does_item_exist(app_data):
        dpg.delete_item(app_data)

def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    first_node = dpg.get_item_user_data(app_data[0])
    second_node = dpg.get_item_user_data(app_data[1])
    is_connected = graph_manager.connect(first_node[0], first_node[1], 
                          second_node[0], second_node[1])
    if is_connected:
        tag = f"{first_node[0]}_{second_node[0]}_{first_node[1]}_{second_node[1]}"
        dpg.add_node_link( app_data[0], app_data[1], parent=sender, 
                          user_data=[first_node[1], second_node[1]], tag=tag)


def delete_node(node_id:str, node_index:int):
    ui_manager.remove_node_ui(node_id)
    node_factory.delete_node(node_id.split("_")[0], node_index)
    graph_manager.remove_node(node_id)


def save_graph_callback():
    if graph_manager.nodes.__len__() == 0:

        logs_handler.add_log("Graph is empty", 1)
        return
    if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_json_save"):
        dpg.show_item(f"{OPENFILE_DIALOG_TAG}_json_save")    
        logs_handler.add_log("Saving Graph....")

def load_graph_callback():
    if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_json_open"):
        dpg.show_item(f"{OPENFILE_DIALOG_TAG}_json_open")
        logs_handler.add_log("Loading Graph")


def delete_selected_nodes(sender, app_data, user_data):
    selected_nodes = dpg.get_selected_nodes(user_data)
    print(selected_nodes, app_data, sender, user_data)
    for item_id in selected_nodes:
        node_user_data = dpg.get_item_user_data(item_id)
        node_index = int(node_user_data[0].split("_")[-1])
        delete_node(node_user_data[0], node_index)

def setup_ui():
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Delete, 
                                    callback=delete_selected_nodes, 
                                    user_data=NODE_EDITOR_TAG)
    
    plot_area.plot_setup()  
        # -------------------------
        # Footer: Bottom 30%
        # -------------------------
    open_file_dialog("json_save", [], save_jsonfile_dialog_callback, "Save Graph As")
    open_file_dialog("json_open", [], open_jsonfile_dialog_callback, "Open Saved Graph")
    with dpg.window(tag=LOG_WINDOW_TAG, 
                    label="Logs", 
                    no_close=True, 
                    no_collapse=True):
        pass
    with dpg.window(tag=EDITOR_TAG, 
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
                        for category, node_configs in nodes_by_category.items():
                            with dpg.tree_node(label=f"{category} Nodes"):
                                for config in node_configs:
                                    dpg.add_button(label=config["drag_btn_name"], width=-1)
                                    with dpg.drag_payload(parent=dpg.last_item(), drag_data=config["drag_id"]):
                                        dpg.add_text(config["drag_text"])

                        
                
                with dpg.child_window(
                                        tag=NODE_EDITOR_PANEL_TAG, 
                                        border=False, 
                                        drop_callback=add_node_callback,
                                        no_scrollbar=True,
                                        no_scroll_with_mouse=True):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="execute graph", callback=lambda: execute_graph())
                        dpg.add_button(label="save graph", callback= lambda : save_graph_callback())
                        dpg.add_button(label="load graph", callback= lambda : load_graph_callback())
                    with dpg.node_editor(tag=NODE_EDITOR_TAG, 
                                        callback=link_callback, 
                                        delink_callback=delink_callback,
                                        minimap=True):
                        with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                            pass