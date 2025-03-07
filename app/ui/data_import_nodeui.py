import dearpygui.dearpygui as dpg
from app.utils.constants import OPENFILE_DIALOG_TAG
    

from app.ui.base_node_ui import BaseNodeUI

class CSVImportNodeUI(BaseNodeUI):
    
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()

    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       mousebutton=dpg.mvMouseButton_Right,
                       parent=self.node_id):
            dpg.add_text("CSV Import Node")
            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_input_text(label="File Path", hint="Enter the file path here.",
                                   tag=f"{self.INPUT_TAG}_{self.node_id}_filepath")                
                dpg.add_button(label="Browse", 
                               )
                
            dpg.add_checkbox(label="Headers", default_value=True, 
                             tag=f"{self.ACTION_TAG}_{self.node_id}_header")
            dpg.add_radio_button(["Comma", "Tab", "Semi-colon", "Colon"],label="Delimit", 
                                 horizontal=True, default_value="Comma", 
                                 tag=f"{self.ACTION_TAG}_{self.node_id}_delimit")
            dpg.add_input_text(label="Target Column", hint="Enter the fit target column here.",
                                tag=f"{self.INPUT_TAG}_{self.node_id}_target")
            
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="X-axis Column", hint="Enter the column with x-axis data.",
                                    tag=f"{self.INPUT_TAG}_{self.node_id}_xaxis")
                dpg.add_checkbox(label="Drop X-axis", default_value=False, 
                                 tag=f"{self.ACTION_TAG}_{self.node_id}_drop")
            
            dpg.add_input_text(label="Drop Columns", hint="Enter the columns to drop sperated by comma.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_drop_cols")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["filepath"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_filepath").strip()
        self.node_instance.params["target_col"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_target").strip()
        self.node_instance.params["xaxis_col"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_xaxis").strip()
        self.node_instance.params["header"] = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_header")
        self.node_instance.params["drop_xaxis"] = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_drop")
        drop_cols = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_drop_cols")
        if len(drop_cols.strip()) == 0:
            self.node_instance.params["drop_cols"] = []
        else:
            self.node_instance.params["drop_cols"] = [col.strip() for col in drop_cols.split(",")]
        
        radio_tag = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}")
        if radio_tag == "Comma":
            self.node_instance.params["csv_sep"] = ","
        elif radio_tag == "Tab":
            self.node_instance.params["csv_sep"] = "\t"
        elif radio_tag == "Semi-colon":
            self.node_instance.params["csv_sep"] = ";"
        elif radio_tag == "Colon":
            self.node_instance.params["csv_sep"] = ":"
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_filepath",
                  self.node_instance.params["filepath"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_target",
                    self.node_instance.params["target_col"])

        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_xaxis",
                    self.node_instance.params["xaxis_col"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_drop_cols",
                    ", ".join(self.node_instance.params["drop_cols"]))
        dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_header",
                    self.node_instance.params["header"])
        dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_drop",
                    self.node_instance.params["drop_xaxis"])
        
        radio_value = self.node_instance.params["csv_sep"]

        if radio_value == ",":
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_delimit", "Comma")
        elif radio_value == "\t":
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_delimit", "Tab")
        elif radio_value == ";":
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_delimit", "Semi-colon")
        elif radio_value == ":":
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_delimit", "Colon")
    
    



class SQLDBImportNodeUI(BaseNodeUI):
    
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()

    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("SQL Import Node")
            dpg.add_separator()

            dpg.add_input_text(label="Connection String", hint="Enter the DB connection string here.",
                                   tag=f"{self.INPUT_TAG}_{self.node_id}_conn")
            dpg.add_input_text(label="Data Query", hint="Enter importing data query here.",
                                   tag=f"{self.INPUT_TAG}_{self.node_id}_data")
            dpg.add_input_text(label="Target Query", hint="Enter importing target query here.",
                                   tag=f"{self.INPUT_TAG}_{self.node_id}_target")
            dpg.add_input_text(label="X-axis Query", hint="Enter importing x-axis data query here.",
                                   tag=f"{self.INPUT_TAG}_{self.node_id}_xaxis")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["conn"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_conn").strip()
        self.node_instance.params["data_query"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_data").strip()
        self.node_instance.params["target_query"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_target").strip()
        self.node_instance.params["xaxis_query"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_xaxis").strip()
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_conn",
                  self.node_instance.params["conn"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_data",
                    self.node_instance.params["data_query"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_target",
                    self.node_instance.params["target_query"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_xaxis",
                    self.node_instance.params["xaxis_query"])