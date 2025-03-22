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
from app.utils.node_config import NODE_CONFIG, PLOT_NODES
from app.utils.plots_config import PLOT_CONFIG
from collections import defaultdict
from app.utils import utils


class NodeEditor:
    def __init__(self):
        self.NODE_UI_MAPPING = { key: config["ui_class"] for key, config in NODE_CONFIG.items() }
        self.NODE_IDS = { key: f"{config['prototype_id']}{dpg.generate_uuid()}" for key, config in NODE_CONFIG.items() }
        self.NODE_CLASS = { key: config["node_class"] for key, config in NODE_CONFIG.items() }
        self.PLOT_NODES = PLOT_NODES

        self.nodes_by_category = defaultdict(list)
        for node_name, config in NODE_CONFIG.items():
            self.nodes_by_category[config["category"]].append(config)

        self.ui_manager = NodeUIManager(self.NODE_UI_MAPPING)
        self.graph_manager = GraphManager()
        self.node_factory = NodeFactory()
        self.logs_handler: LogHandler = LogHandler()
        self.selected_nodes = []

        self.plot_area: PlotArea = PlotArea(PLOT_CONFIG)

        for key in self.NODE_CLASS:
            self.node_factory.register_prototype(key, self.NODE_CLASS[key](self.NODE_IDS[key]))

        self.examples_folder = utils.get_examples_folder()

    def __call__(self):
        self.setup_ui()

    def execute_graph(self):
        dpg.disable_item("save_computation")
        if self.graph_manager.execute():
            try:
                for node_id in self.graph_manager.nodes.keys():
                    node:Node = self.graph_manager.get_node(node_id)
                    self.ui_manager.update_node_ui(node_id)
                    if node.__class__.__name__ in self.PLOT_NODES:
                        if node.has_data:
                            self.plot_area.plot_manager.plot(node.params, node.plot_data)
                    
                self.logs_handler.add_log("Graph executed successfully.")
                dpg.enable_item("save_computation")
            except Exception as e:
                self.logs_handler.add_log(f"Error executing graph: {e}", -1)
            

    def get_relative_mouse_pos(self, ref_object:str):
        global_mouse_pos = dpg.get_mouse_pos(local=False)
            
        dpg.show_item(ref_object)
        dpg.split_frame()  
        ref_rect_min = dpg.get_item_rect_min(ref_object)
        ref_grid_pos = dpg.get_item_pos(ref_object)
        dpg.hide_item(ref_object)
        local_x = global_mouse_pos[0] - ref_rect_min[0] + ref_grid_pos[0]
        local_y = global_mouse_pos[1] - ref_rect_min[1] + ref_grid_pos[1]
        return [local_x, local_y]


    def open_csvfile_dialog_callback(self, sender, app_data, user_data):
        input_text_tag = user_data
        selected_file = list(app_data['selections'].items())[0][1]
        if dpg.does_item_exist(input_text_tag):
            dpg.set_value(input_text_tag, selected_file)

    def save_jsonfile_dialog_callback(self, sender, app_data, user_data):
        selected_file = app_data["file_path_name"].split(".")[0] + ".json"
        if len(selected_file) == 0:
            return
        for node_id in self.graph_manager.nodes.keys():
            self.ui_manager.set_current_pos(node_id)
        self.graph_manager.save_to_file(selected_file, self.node_factory)
        self.logs_handler.add_log("Graph saved successfully.")

    def load_graph(self, graph_file:str):
        if os.path.exists(graph_file):
            node_ids = [ky for ky in self.graph_manager.nodes.keys()]
            for node_id in node_ids:
                node = self.graph_manager.get_node(node_id)
                self.delete_node(node.node_id, node.node_index)
            self.graph_manager.load_from_file(graph_file, self.node_factory)
            self.create_loaded_nodes()
            self.logs_handler.add_log("Graph loaded successfully.")
        else:
            self.logs_handler.add_log(f"File: {graph_file} not found.", -1)

    def open_jsonfile_dialog_callback(self, sender, app_data, user_data):
        self.logs_handler.add_log("Loading Graph")
        selected_file = None
        if app_data["selections"].__len__() > 0:
            selected_file = list(app_data['selections'].items())[0][1]
        else:
            selected_file = app_data["file_path_name"]
        self.load_graph(selected_file)

    def open_folder_dialog_callback(self, sender, app_data, user_data):
        selected_folder = app_data["file_path_name"]
        if len(selected_folder) == 0:
            self.logs_handler.add_log("No folder selected.", 1)
            return
        if os.path.exists(selected_folder):
            for node_id in self.graph_manager.nodes.keys():
                node:Node = self.graph_manager.get_node(node_id)
                node.save_node_results(selected_folder)
            self.logs_handler.add_log(f"Saved Computed Data in: {selected_folder}")

    def open_folder_dialog(self, tag:str, user_data:str, callback, label="Select Folder"):
        with dpg.file_dialog(
                            label=label, directory_selector=True, show=False, 
                            tag=f"{OPENFILE_DIALOG_TAG}_{tag}", width=520 ,
                            height=400, modal=True, user_data=user_data,
                            callback=callback):
            pass

    def open_file_dialog(self, tag:str, user_data:str, callback, label="Open File"):
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


    def create_nodes_copy(self, node_ids:list[str]):
        dpg.disable_item("save_computation")
        created_nodes = {}
        
        mouse_pos = self.get_relative_mouse_pos(REF_NODE_TAG)
        def get_new_pos(m_pos, n_pos):
            
            new_x = m_pos[0] - n_pos[0]
            new_y = m_pos[1] - n_pos[1]
            return [new_x, new_y]
        off_set = [0, 0]
        for node_id in node_ids:
            node : Node = self.graph_manager.get_node(node_id)
            if created_nodes.__len__() == 0:
                if dpg.is_item_hovered(NODE_EDITOR_TAG):
                    off_set = get_new_pos(mouse_pos, node.position)
                else:
                    off_set = get_new_pos([node.position[0], node.position[1] + 200], 
                                        node.position)
            if not node_id in created_nodes:
                self.ui_manager.set_current_pos(node_id)
                new_pos = [node.position[0] + off_set[0], node.position[1] + off_set[1]]
                new_node : Node = self.node_factory.create_node(node.__class__.__name__, new_pos)
                new_node.params.update(node.params)
                self.graph_manager.add_node(new_node)
                self.ui_manager.create_node_ui(new_node)
                self.ui_manager.update_node_ui(new_node.node_id)

                created_nodes[node_id] = new_node
            
            for port in node.input_ports:
                if port.connection is not None:
                    id_split = port.connection.split("_")
                    con_node_id = f'{id_split[1]}_{id_split[2]}'
                    if con_node_id in node_ids:
                        con_node = self.graph_manager.get_node(con_node_id)
                        if not con_node_id in created_nodes:
                            self.ui_manager.set_current_pos(con_node_id)
                            new_pos = [con_node.position[0] + off_set[0], con_node.position[1] + off_set[1]]
                            new_con_node = self.node_factory.create_node(con_node.__class__.__name__, new_pos)
                            new_con_node.params.update(con_node.params)
                            self.graph_manager.add_node(new_con_node)
                            self.ui_manager.create_node_ui(new_con_node)
                            self.ui_manager.update_node_ui(new_con_node.node_id)
                            created_nodes[con_node_id] = new_con_node
                        
                        con_port_index = con_node.get_output_port_index(port.connection)
                        new_source_id = created_nodes[con_node_id].node_id
                        new_source_port_id = created_nodes[con_node_id].output_ports[con_port_index].port_id
                        new_target_id = created_nodes[node_id].node_id
                        new_target_port_id = created_nodes[node_id].input_ports[port.port_index].port_id

                        self.graph_manager.connect(new_source_id, new_source_port_id, new_target_id, new_target_port_id)
                        self.reconnect_loaded_nodes(new_source_id, new_target_id, new_source_port_id, new_target_port_id)
            

    def add_node_callback(self, sender, app_data, user_data):
        dpg.disable_item("save_computation")
        pos = self.get_relative_mouse_pos(REF_NODE_TAG)
        node = self.node_factory.create_node(app_data, pos)
        self.graph_manager.add_node(node)
        self.ui_manager.create_node_ui(node)


    def create_loaded_nodes(self):
        for node_id, node in self.graph_manager.nodes.items():
            self.ui_manager.create_node_ui(node)
            self.ui_manager.update_node_ui(node_id)
        
        for conn in self.graph_manager.connections:
            self.reconnect_loaded_nodes(conn[0], conn[2], conn[1], conn[3])


    def reconnect_loaded_nodes(self, node_1, node_2, port_1, port_2):
        attr_1 = port_1 
        attr_2 = port_2
        tag = f"{node_1}_{node_2}_{attr_1}_{attr_2}" 
        dpg.add_node_link(attr_1, attr_2, parent=NODE_EDITOR_TAG, user_data=[port_1, port_2], tag=tag)
        self.ui_manager.connect_ports(node_2, port_2)

        
    def delink_callback(self, sender, app_data, user_data):
        # app_data -> link_id
        ports = dpg.get_item_user_data(app_data)
        self.graph_manager.disconnect(ports[0], ports[1])
        split = ports[1].split("_")
        node_id = f"{split[1]}_{split[2]}"
        self.ui_manager.disconnect_ports(node_id, ports[1])

        if dpg.does_item_exist(app_data):
            dpg.delete_item(app_data)

    def link_callback(self, sender, app_data):
        # app_data -> (link_id1, link_id2)
        first_node = dpg.get_item_user_data(app_data[0])
        second_node = dpg.get_item_user_data(app_data[1])
        is_connected = self.graph_manager.connect(first_node[0], first_node[1], 
                            second_node[0], second_node[1])
        if is_connected:
            lastest_con = self.graph_manager.connections[-1]
            tag = f"{lastest_con[0]}_{lastest_con[2]}_{lastest_con[1]}_{lastest_con[3]}"
            dpg.add_node_link( app_data[0], app_data[1], parent=sender, 
                            user_data=[lastest_con[1], lastest_con[3]], tag=tag)
            self.ui_manager.connect_ports(lastest_con[2], lastest_con[3])


    def delete_node(self, node_id:str, node_index:int):
        dpg.disable_item("save_computation")
        self.ui_manager.remove_node_ui(node_id)
        self.node_factory.delete_node(node_id.split("_")[0], node_index)
        self.graph_manager.remove_node(node_id)


    def save_graph_callback(self):
        if len(self.graph_manager.nodes) == 0:
            self.logs_handler.add_log("Graph is empty", 1)
            return
        if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_json_save"):
            dpg.show_item(f"{OPENFILE_DIALOG_TAG}_json_save")    
            self.logs_handler.add_log("Saving Graph....")

    def folder_dialog_callback(self):
        if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_select_folder"):
            dpg.show_item(f"{OPENFILE_DIALOG_TAG}_select_folder")

    def load_graph_callback(self):
        if dpg.does_item_exist(f"{OPENFILE_DIALOG_TAG}_json_open"):
            dpg.disable_item("save_computation")
            dpg.show_item(f"{OPENFILE_DIALOG_TAG}_json_open")
            

    def paste_callback(self, sender, app_data, user_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            if len(self.selected_nodes) > 0:
                self.create_nodes_copy(self.selected_nodes)
            self.selected_nodes.clear()

    def copy_callback(self, sender, app_data, user_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            sel_nodes = dpg.get_selected_nodes(NODE_EDITOR_TAG)
            self.selected_nodes = [dpg.get_item_user_data(node_id)[0] for node_id in sel_nodes]

    def load_shorcut_callback(self, sender, app_data, user_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            self.load_graph_callback()

    def save_shorcut_callback(self, sender, app_data, user_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            self.save_graph_callback()


    def load_example_callback(self, sender, app_data, user_data):
        examples_file = os.path.join(self.examples_folder, user_data)
        self.load_graph(examples_file)


    def delete_selected_nodes(self, sender, app_data, user_data):
        dpg.disable_item("save_computation")
        selected = dpg.get_selected_nodes(user_data)
        for item_id in selected:
            node_user_data = dpg.get_item_user_data(item_id)
            node_index = int(node_user_data[0].split("_")[-1])
            self.delete_node(node_user_data[0], node_index)

    def main_menu(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File   "):
                dpg.add_menu_item(label="Save       Ctrl+S", callback=self.save_graph_callback)
                dpg.add_menu_item(label="Load       Ctrl+O", callback=self.load_graph_callback)
                dpg.add_separator()
                dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)

            with dpg.menu(label="Edit   "):
                dpg.add_menu_item(label="Copy       Ctrl+C", callback=self.copy_callback)
                dpg.add_menu_item(label="Paste      Ctrl+V", callback=self.paste_callback)
                dpg.add_menu_item(label="Delete     Del", callback=self.delete_selected_nodes, user_data=NODE_EDITOR_TAG)

            with dpg.menu(label="Help   "):
                dpg.add_menu_item(label="About      ", callback=lambda: self.logs_handler.add_log("About: This is a simple data analysis tool."))
                with dpg.menu(label="Examples       "):
                    dpg.add_menu_item(label="Classification", callback=self.load_example_callback, user_data="classification_example.json")
                    dpg.add_menu_item(label="Clustering",  callback=self.load_example_callback, user_data="clustering_example.json")
                    dpg.add_menu_item(label="Regression",  callback=self.load_example_callback, user_data="regression_example.json")

    def setup_ui(self):
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Delete, callback=self.delete_selected_nodes, user_data=NODE_EDITOR_TAG)
            dpg.add_key_press_handler(callback=self.copy_callback, key=dpg.mvKey_C)
            dpg.add_key_press_handler(callback=self.paste_callback, key=dpg.mvKey_V)
            dpg.add_key_press_handler(callback=self.load_shorcut_callback, key=dpg.mvKey_O)
            dpg.add_key_press_handler(callback=self.save_shorcut_callback, key=dpg.mvKey_S)
        self.main_menu()
        self.plot_area.plot_setup()
        # Footer: create dialogs and log window
        self.open_file_dialog("json_save", [], self.save_jsonfile_dialog_callback, "Save Graph As")
        self.open_file_dialog("json_open", [], self.open_jsonfile_dialog_callback, "Open Saved Graph")
        self.open_folder_dialog("select_folder", [], self.open_folder_dialog_callback, "Select Folder")
        with dpg.window(tag=LOG_WINDOW_TAG, label="Logs", no_close=True, no_collapse=True):
            pass
        with dpg.window(tag=EDITOR_TAG, label="Editor", no_close=True, no_collapse=True, no_scrollbar=True, no_scroll_with_mouse=True):
            with dpg.table(header_row=False, borders_innerV=True, resizable=True):
                dpg.add_table_column(width=300)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(tag=FUNCTIONS_PANEL_TAG, border=False):
                        with dpg.group():
                            for category, node_configs in self.nodes_by_category.items():
                                with dpg.tree_node(label=f"{category} Nodes"):
                                    for config in node_configs:
                                        dpg.add_button(label=config["drag_btn_name"], width=-1)
                                        with dpg.drag_payload(parent=dpg.last_item(), drag_data=config["drag_id"]):
                                            dpg.add_text(config["drag_text"])
                    with dpg.child_window(tag=NODE_EDITOR_PANEL_TAG, border=False, drop_callback=self.add_node_callback, no_scrollbar=True, no_scroll_with_mouse=True):
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="execute graph", callback=lambda: self.execute_graph())
                            dpg.add_button(label="save graph", callback=lambda: self.save_graph_callback())
                            dpg.add_button(label="load graph", callback=lambda: self.load_graph_callback())
                            dpg.add_button(label="save computation", enabled=False, tag="save_computation", callback=lambda: self.folder_dialog_callback())
                        with dpg.node_editor(tag=NODE_EDITOR_TAG, callback=self.link_callback, delink_callback=self.delink_callback, minimap=True):
                            with dpg.node(label="giberish", tag=REF_NODE_TAG, pos=(0, 0), show=False):
                                pass