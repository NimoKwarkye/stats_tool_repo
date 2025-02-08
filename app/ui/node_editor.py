import dearpygui.dearpygui as dpg
from app.core.node import Node
from app.core.graph_manager import GraphManager
from app.core.node_factory import NodeFactory
from app.nodes.data_import_node import CSVImportNode
from app.nodes.linear_regression_node import LinearRegressionNode


MAIN_WINDOW_TAG       = "MainWindow"
PLOT_AREA_TAG         = "PlotArea"
FOOTER_TAG            = "Footer"
FUNCTIONS_PANEL_TAG   = "FunctionsPanel"
NODE_EDITOR_PANEL_TAG = "NodeEditorPanel"
NODE_EDITOR_TAG       = "node_editor"
OPENFILE_DIALOG_TAG   = "open_file_dialog"
INPUT_TEXT_TAG        = "input_text"
POP_UP_TAG            = "pop_up"
CSV_RADIO_TAG         = "csv_radio"
REF_NODE_TAG = "ref_node"
CSVIMPORT_DRAG_ID = "CSVImport"
LINEAR_REG_DRAG_ID = "LinRegression"


graph_manager = GraphManager()
node_factory = NodeFactory()

node_factory.register_prototype(CSVIMPORT_DRAG_ID, CSVImportNode("proto_csv"))
node_factory.register_prototype(LINEAR_REG_DRAG_ID, LinearRegressionNode("proto_lin_reg"))


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


def open_file_dialog_callback(sender, app_data, user_data):
    input_text_tag = user_data
    selected_file = list(app_data['selections'].items())[0][1]
    dpg.set_value(input_text_tag, selected_file)

def open_file_dialog(node_instance:Node):
    with dpg.file_dialog(directory_selector=False, show=False, 
                         tag=f"{OPENFILE_DIALOG_TAG}_{node_instance.node_id}", width=700 ,
                         height=400, modal=True, user_data=f"{INPUT_TEXT_TAG}_{node_instance.node_id}",
                         callback=open_file_dialog_callback):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.csv){.csv}", color=(0, 255, 255, 255))
        dpg.add_file_extension(".csv", color=(255, 0, 255, 255), custom_text="[CSV]")


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
    elif radio_tag == "colon":
        node_instance.params["csv_sep"] = ":"
        


def add_node_popup(node_instance:Node):

    if node_instance.__class__.__name__ == "CSVImportNode":

        with dpg.popup(parent=node_instance.node_id, tag=f"{POP_UP_TAG}_{node_instance.node_id}"):
            dpg.add_text("CSV Import Node")
            dpg.add_text("Select a CSV file to import.")
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="File Path", hint="Enter the file path here.",
                                   tag=f"{INPUT_TEXT_TAG}_{node_instance.node_id}")
                dpg.add_button(label="Browse", callback=lambda:dpg.show_item(f"{OPENFILE_DIALOG_TAG}_{node_instance.node_id}"))
            dpg.add_radio_button(["Comma", "Tab", "Semi-colon", "colon"],label="Delimit", 
                                 horizontal=True, default_value="Comma", tag=f"{CSV_RADIO_TAG}_{node_instance.node_id}")
            dpg.add_button(label="Save", callback=csv_import_callback, user_data=node_instance)


def add_node_callback(sender, app_data, user_data):

    pos = get_relative_mouse_pos(REF_NODE_TAG)
    node = node_factory.create_node(app_data, pos)
    new_id = node.node_id
    graph_manager.add_node(node)
    open_file_dialog(node)
    # Create a visual node using dearpygui's node editor.
    with dpg.node(label=f"{node.name} {node.node_index}", tag=new_id, 
                  parent=NODE_EDITOR_TAG, pos=pos, user_data=[new_id, app_data]):
        add_node_popup(node)
        for att in node.input_ports:
            with dpg.node_attribute(label=att.name,
                                   parent=new_id,
                                   attribute_type=dpg.mvNode_Attr_Input,
                                   user_data=[new_id, att.name]):
                dpg.add_text(att.name)

        for att in node.output_ports:
            with dpg.node_attribute(label=att.name,
                                   parent=new_id,
                                   attribute_type=dpg.mvNode_Attr_Output,
                                   user_data=[new_id, att.name]):
                dpg.add_text(att.name)


def delink_callback(sender, app_data, user_data):
        # app_data -> link_id
    graph_manager.disconnect(dpg.get_item_user_data(app_data)[0])
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

def delete_selected_nodes(self, sender, app_data, user_data):
    selected_nodes = dpg.get_selected_nodes(app_data)
    
    for item_id in selected_nodes:
        node_user_data = dpg.get_item_user_data(item_id)
        node_index = int(node_user_data[0].split("_")[-1])
        graph_manager.remove_node(node_user_data[0])
        node_factory.delete_node(node_user_data[1], node_index)
        dpg.delete_item(f"{OPENFILE_DIALOG_TAG}_{node_user_data[0]}")
        dpg.delete_item(f"{POP_UP_TAG}_{node_user_data[0]}")
        dpg.delete_item(node_user_data[0])

def setup_ui():
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Delete, 
                                    callback=delete_selected_nodes, 
                                    user_data=NODE_EDITOR_TAG)
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
                        btn_data_loader = dpg.add_button(label="Data Loader")
                        btn_xy_data_loader = dpg.add_button(label="Import XY Data")
                        btn_linear_regression = dpg.add_button(label="Simple LR")
                        with dpg.drag_payload(parent=btn_data_loader):
                            dpg.add_text("New Data Loader")
                        with dpg.drag_payload(parent=btn_xy_data_loader,
                                              drag_data=CSVIMPORT_DRAG_ID):
                            dpg.add_text("New XY Data Loader")
                        with dpg.drag_payload(parent=btn_linear_regression,
                                              drag_data=LINEAR_REG_DRAG_ID):
                            dpg.add_text("Add a Simple Linear Regression Node")
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
                    with dpg.node_editor(tag=NODE_EDITOR_TAG, 
                                        callback=link_callback, 
                                        delink_callback=delink_callback,
                                        minimap=True):
                        with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                            pass