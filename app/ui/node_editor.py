import dearpygui.dearpygui as dpg
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


def add_node_callback(sender, app_data, user_data):

    new_id = f"node_{len(graph_manager.nodes)+1}"
    pos = get_relative_mouse_pos(REF_NODE_TAG)
    node = node_factory.create_node(app_data, new_id, pos)
    graph_manager.add_node(node)

    # Create a visual node using dearpygui's node editor.
    with dpg.node(label=node.name, tag=new_id, parent=NODE_EDITOR_TAG, pos=pos, user_data=new_id):
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
        node_id = dpg.get_item_user_data(item_id)
        print(node_id)
        graph_manager.remove_node(node_id)
        dpg.delete_item(node_id)

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