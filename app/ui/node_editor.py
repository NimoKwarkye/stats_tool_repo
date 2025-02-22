import os
import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.core.graph_manager import GraphManager
from app.core.node_factory import NodeFactory
from app.nodes.data_import_node import CSVImportNode
from app.nodes.linear_regression_node import LinearRegressionNode
from app.nodes.data_plots_nodes import XYScatterPlotNode
from app.ui import plot_area
from app.utils.log_handler import LogHandler 
from app.utils.constants import EDITOR_TAG, FUNCTIONS_PANEL_TAG, NODE_EDITOR_PANEL_TAG, \
                                NODE_EDITOR_TAG, OPENFILE_DIALOG_TAG, INPUT_TEXT_TAG, \
                                POP_UP_TAG, CSV_RADIO_TAG, REF_NODE_TAG, CSVIMPORT_DRAG_ID, \
                                LINEAR_REG_DRAG_ID, SCATTER_PLOT_DRAG_ID, PLOT_1_TAG,\
                                PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG, \
                                INPUT_TEXT_TAG, PLOT_TITLE_TEXT_TAG, XLABEL_TEXT_TAG, YLABEL_TEXT_TAG, \
                                PLOT_TYPE_RADIO_TAG, PLOT_REGION_TAG, PLOT_MARKER_COLOR_TAG, \
                                PLOT_LINE_COLOR_TAG, PLOT_COLORMAP_TAG, LOG_WINDOW_TAG




graph_manager = GraphManager()
node_factory = NodeFactory()
logs_handler: LogHandler = LogHandler()

node_factory.register_prototype(CSVIMPORT_DRAG_ID, CSVImportNode("proto_csv"))
node_factory.register_prototype(LINEAR_REG_DRAG_ID, LinearRegressionNode("proto_lin_reg"))
node_factory.register_prototype(SCATTER_PLOT_DRAG_ID, XYScatterPlotNode("proto_scatter_plot"))

def execude_graph():
    if graph_manager.execute():
        for node_id in graph_manager.nodes.keys():
            node:Node = graph_manager.get_node(node_id)
            if node.__class__.__name__ == "XYScatterPlotNode":
                if node.has_data:
                    plot_area.scatter_plot(node.params["region"], node.params, node.plot_data)
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
        for node_id in node_ids:
            delete_node(graph_manager.get_node(node_id))
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


def csv_import_callback(sender, app_data, user_data):
    node_instance:Node = user_data
    node_instance.params["filepath"] = dpg.get_value(f"{INPUT_TEXT_TAG}_{node_instance.node_id}")
    radio_tag = dpg.get_value(f"{CSV_RADIO_TAG}_{node_instance.node_id}")
    if radio_tag == "Comma":
        node_instance.params["csv_sep"] = ","
    elif radio_tag == "Tab":
        node_instance.params["csv_sep"] = "\t"
    elif radio_tag == "Semi-colon":
        node_instance.params["csv_sep"] = ";"
    elif radio_tag == "Colon":
        node_instance.params["csv_sep"] = ":"

def csv_import_ui_update(node_instance:Node):
    dpg.set_value(f"{INPUT_TEXT_TAG}_{node_instance.node_id}",
                  node_instance.params["filepath"])
    radio_value = node_instance.params["csv_sep"]

    if radio_value == ",":
        dpg.set_value(f"{CSV_RADIO_TAG}_{node_instance.node_id}", "Comma")
    elif radio_value == "\t":
        dpg.set_value(f"{CSV_RADIO_TAG}_{node_instance.node_id}", "Tab")
    elif radio_value == ";":
        dpg.set_value(f"{CSV_RADIO_TAG}_{node_instance.node_id}", "Semi-colon")
    elif radio_value == ":":
        dpg.set_value(f"{CSV_RADIO_TAG}_{node_instance.node_id}", "Colon")
    
def xy_scatter_plot_ui_update(node_instance:Node):
    dpg.set_value(f"{PLOT_TITLE_TEXT_TAG}_{node_instance.node_id}", node_instance.params["title"])
    dpg.set_value(f"{XLABEL_TEXT_TAG}_{node_instance.node_id}", node_instance.params["xlabel"])
    dpg.set_value(f"{YLABEL_TEXT_TAG}_{node_instance.node_id}", node_instance.params["ylabel"])
    dpg.set_value(f"{PLOT_MARKER_COLOR_TAG}_{node_instance.node_id}", node_instance.params["marker_color"])
    dpg.set_value(f"{PLOT_LINE_COLOR_TAG}_{node_instance.node_id}", node_instance.params["line_color"])
    region = node_instance.params["region"]
    if region == PLOT_1_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 1")
    elif region == PLOT_2_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 2")
    elif region == PLOT_3_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 3")
    elif region == PLOT_4_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 4")
    elif region == PLOT_5_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 5")
    elif region == PLOT_6_TAG:
        dpg.set_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}", "Plot 6")

def update_node_ui_params(node_instance: Node):
    if node_instance.__class__.__name__ == "CSVImportNode":
        csv_import_ui_update(node_instance)
    elif node_instance.__class__.__name__ == "XYScatterPlotNode":
        xy_scatter_plot_ui_update(node_instance)


def scatter_plot_callback(sender, app_data, user_data):
    node_instance:Node = user_data
    node_instance.params["title"] = dpg.get_value(f"{PLOT_TITLE_TEXT_TAG}_{node_instance.node_id}")
    node_instance.params["xlabel"] = dpg.get_value(f"{XLABEL_TEXT_TAG}_{node_instance.node_id}")
    node_instance.params["ylabel"] = dpg.get_value(f"{YLABEL_TEXT_TAG}_{node_instance.node_id}")
    node_instance.params["marker_color"] = dpg.get_value(f"{PLOT_MARKER_COLOR_TAG}_{node_instance.node_id}")
    node_instance.params["line_color"] = dpg.get_value(f"{PLOT_LINE_COLOR_TAG}_{node_instance.node_id}")
    rg = dpg.get_value(f"{PLOT_REGION_TAG}_{node_instance.node_id}")
    if rg == "Plot 1":
        node_instance.params["region"] = PLOT_1_TAG
    elif rg == "Plot 2":
        node_instance.params["region"] = PLOT_2_TAG
    elif rg == "Plot 3":
        node_instance.params["region"] = PLOT_3_TAG
    elif rg == "Plot 4":
        node_instance.params["region"] = PLOT_4_TAG
    elif rg == "Plot 5":
        node_instance.params["region"] = PLOT_5_TAG
    elif rg == "Plot 6":
        node_instance.params["region"] = PLOT_6_TAG

def add_node_popup(node_instance:Node):

    if node_instance.__class__.__name__ == "CSVImportNode":

        with dpg.popup(parent=node_instance.node_id, tag=f"{POP_UP_TAG}_{node_instance.node_id}", modal=False):
            dpg.add_text("CSV Import Node")
            dpg.add_text("Select a CSV file to import.")
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="File Path", hint="Enter the file path here.",
                                   tag=f"{INPUT_TEXT_TAG}_{node_instance.node_id}")
                dpg.add_button(label="Browse", callback=lambda:dpg.show_item(f"{OPENFILE_DIALOG_TAG}_{node_instance.node_id}"))
            dpg.add_radio_button(["Comma", "Tab", "Semi-colon", "Colon"],label="Delimit", 
                                 horizontal=True, default_value="Comma", tag=f"{CSV_RADIO_TAG}_{node_instance.node_id}")
            dpg.add_button(label="Save Changes", callback=csv_import_callback, user_data=node_instance)
    
    elif node_instance.__class__.__name__ == "LinearRegressionNode":
        with dpg.popup(parent=node_instance.node_id, tag=f"{POP_UP_TAG}_{node_instance.node_id}", modal=False):
            dpg.add_text("Linear Regression Node")
            dpg.add_text("This node will compute the slope and intercept of a given data set.")
    
    elif node_instance.__class__.__name__ == "XYScatterPlotNode":
        with dpg.popup(parent=node_instance.node_id, tag=f"{POP_UP_TAG}_{node_instance.node_id}", modal=False):
            dpg.add_text("XY Scatter Plot Node")
            dpg.add_input_text(label="Title", hint="Enter the plot title here.", tag=f"{PLOT_TITLE_TEXT_TAG}_{node_instance.node_id}")
            dpg.add_input_text(label="X Label", hint="Enter the x-axis label here.", tag=f"{XLABEL_TEXT_TAG}_{node_instance.node_id}")
            dpg.add_input_text(label="Y Label", hint="Enter the y-axis label here.", tag=f"{YLABEL_TEXT_TAG}_{node_instance.node_id}")
            dpg.add_color_edit(label="Marker Color", default_value=(255, 255, 255, 255), 
                               tag=f"{PLOT_MARKER_COLOR_TAG}_{node_instance.node_id}")
            dpg.add_color_edit(label="Line Color", default_value=(255, 0, 255, 255), 
                               tag=f"{PLOT_LINE_COLOR_TAG}_{node_instance.node_id}")
            dpg.add_combo(label="Plot Area", items=["Plot 1", "Plot 2", "Plot 3", "Plot 4", "Plot 5", "Plot 6"], 
                          default_value="Plot 1", tag=f"{PLOT_REGION_TAG}_{node_instance.node_id}")
            dpg.add_button(label="Save Changes", callback=scatter_plot_callback, user_data=node_instance)

def create_node(node : Node, app_data):
    new_id = node.node_id
    pos = node.position
    if node.__class__.__name__ == "CSVImportNode":
        open_file_dialog(node.node_id, 
                         f"{INPUT_TEXT_TAG}_{node.node_id}", 
                         open_csvfile_dialog_callback)
    with dpg.node(label=f"{node.name} {node.node_index}", tag=new_id, 
                  parent=NODE_EDITOR_TAG, pos=pos, user_data=[new_id, app_data]):
        add_node_popup(node)
        for idx, att in enumerate(node.input_ports):
            node.input_ports[idx].port_index = idx
            with dpg.node_attribute(label=att.name,
                                   parent=new_id,
                                   tag = att.name + new_id + f"input_{idx}",
                                   attribute_type=dpg.mvNode_Attr_Input,
                                   user_data=[new_id, att.name]):
                dpg.add_text(att.name.split("##")[0])

        for idx, att in enumerate(node.output_ports):
            node.output_ports[idx].port_index = idx
            with dpg.node_attribute(label=att.name,
                                   parent=new_id,
                                   tag = att.name + new_id + f"output_{idx}",
                                   attribute_type=dpg.mvNode_Attr_Output,
                                   user_data=[new_id, att.name]):
                dpg.add_text(att.name.split("##")[0])

def add_node_callback(sender, app_data, user_data):

    pos = get_relative_mouse_pos(REF_NODE_TAG)
    node = node_factory.create_node(app_data, pos)
    graph_manager.add_node(node)
    
    create_node(node, app_data)


def create_loaded_nodes():
    for node_id, node in graph_manager.nodes.items():
        type_name  = node.node_id.split("_")[0]
        create_node(node, type_name)
        update_node_ui_params(node)
    
    for conn in graph_manager.connections:
        reconnect_loaded_nodes(conn[0], conn[1], conn[2], conn[3])


def reconnect_loaded_nodes(node_id_1, port_1, node_id_2, port_2):
    node_1 = graph_manager.get_node(node_id_1)
    node_2 = graph_manager.get_node(node_id_2)
    attr_1 = port_1 + node_1.node_id + f"output_{node_1.get_output_port_index(port_1)}"
    attr_2 = port_2 + node_2.node_id + f"input_{node_2.get_input_port_index(port_2)}"
    dpg.add_node_link(attr_1, attr_2, parent=NODE_EDITOR_TAG, user_data=[port_1, port_2])

def delink_callback(sender, app_data, user_data):
        # app_data -> link_id
    ports = dpg.get_item_user_data(app_data)
    graph_manager.disconnect(ports[0], ports[1])
    dpg.delete_item(app_data)

def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    first_node = dpg.get_item_user_data(app_data[0])
    second_node = dpg.get_item_user_data(app_data[1])
    is_connected = graph_manager.connect(first_node[0], first_node[1], 
                          second_node[0], second_node[1])
    if is_connected:
        dpg.add_node_link(app_data[0], app_data[1], parent=sender, 
                          user_data=[first_node[1], second_node[1]])


def delete_node(node:Node):
    node_id = node.node_id
    if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_{node_id}"):
        dpg.delete_item(f"{OPENFILE_DIALOG_TAG}_{node_id}")
    if dpg.does_item_exist(f"{POP_UP_TAG}_{node_id}"):
        dpg.delete_item(f"{POP_UP_TAG}_{node_id}")  
    dpg.delete_item(node_id)
    node_factory.delete_node(node_id.split("_")[0], node.node_index)
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



def delete_selected_nodes(self, sender, app_data, user_data):
    selected_nodes = dpg.get_selected_nodes(app_data)
    
    for item_id in selected_nodes:
        node_user_data = dpg.get_item_user_data(item_id)
        node_index = int(node_user_data[0].split("_")[-1])
        
        if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_{node_user_data[0]}"):
            dpg.delete_item(f"{OPENFILE_DIALOG_TAG}_{node_user_data[0]}")
        
        if dpg.does_item_exist(f"{POP_UP_TAG}_{node_user_data[0]}"):
            dpg.delete_item(f"{POP_UP_TAG}_{node_user_data[0]}")
        
        dpg.delete_item(node_user_data[0])
        graph_manager.remove_node(node_user_data[0])
        node_factory.delete_node(node_user_data[1], node_index)

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
                        btn_data_loader = dpg.add_button(label="Data Loader")
                        btn_xy_data_loader = dpg.add_button(label="Import XY Data")
                        btn_linear_regression = dpg.add_button(label="Simple LR")
                        btn_xy_scatter = dpg.add_button(label="XY Scatter Plot")
                        with dpg.drag_payload(parent=btn_data_loader):
                            dpg.add_text("New Data Loader")
                        with dpg.drag_payload(parent=btn_xy_data_loader,
                                              drag_data=CSVIMPORT_DRAG_ID):
                            dpg.add_text("New XY Data Loader")
                        with dpg.drag_payload(parent=btn_linear_regression,
                                              drag_data=LINEAR_REG_DRAG_ID):
                            dpg.add_text("Add a Simple Linear Regression Node")
                        with dpg.drag_payload(parent=btn_xy_scatter,
                                              drag_data=SCATTER_PLOT_DRAG_ID):
                            dpg.add_text("Add a XY Scatter Plot Node")
                        '''with dpg.drag_payload(
                                                parent=btn_b, 
                                                drag_data={"name":"Function B", "value":dpg.mvNode_Attr_Output}):
                            dpg.add_text("Draging Function B")'''
                
                with dpg.child_window(
                                        tag=NODE_EDITOR_PANEL_TAG, 
                                        border=False, 
                                        drop_callback=add_node_callback,
                                        no_scrollbar=True,
                                        no_scroll_with_mouse=True):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="execute graph", callback=lambda: execude_graph())
                        dpg.add_button(label="save graph", callback= lambda : save_graph_callback())
                        dpg.add_button(label="load graph", callback= lambda : load_graph_callback())
                    with dpg.node_editor(tag=NODE_EDITOR_TAG, 
                                        callback=link_callback, 
                                        delink_callback=delink_callback,
                                        minimap=True):
                        with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                            pass