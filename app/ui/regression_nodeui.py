import dearpygui.dearpygui as dpg
from app.ui.base_node_ui import BaseNodeUI



class SimpleLinearRegressionNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()


    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("Simple Linear Regression Node")
            dpg.add_separator()
            dpg.add_input_int(label="degree", 
                              default_value=self.node_instance.params["degree"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_degree", 
                              min_value=1, max_value=10,
                              max_clamped=True, min_clamped=True)
            dpg.add_separator()
            
            dpg.add_input_text(label="Slope", 
                               default_value=str(self.node_instance.params["slope"]),
                               tag=f"{self.INPUT_TAG}_{self.node_id}_slope",
                               readonly=True)
            dpg.add_input_text(label="Intercept", 
                               default_value=str(self.node_instance.params["intercept"]),
                               tag=f"{self.INPUT_TAG}_{self.node_id}_intercept",
                               readonly=True)
            dpg.add_input_text(label="R² Score", 
                               default_value=str(self.node_instance.params["r2_score"]),
                               tag=f"{self.INPUT_TAG}_{self.node_id}_r2_score",
                               readonly=True)
            dpg.add_button(label="Save Changes", callback=self.popup_callback)

    def popup_callback(self):
        self.node_instance.params["degree"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_degree")
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")

    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_slope",
                      self.node_instance.params["slope"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_intercept",
                      self.node_instance.params["intercept"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_r2_score",
                      self.node_instance.params["r2_score"])

        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_degree",
                      self.node_instance.params["degree"])


class LinearRegressionNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()


    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("Linear Regression Node")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_input_float(label="Test Size", 
                                default_value=self.node_instance.params["test_size"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_test_size", 
                                min_value=0.1, max_value=1.0,
                                max_clamped=True, min_clamped=True)
                dpg.add_checkbox(label="Positive Only",
                                default_value=self.node_instance.params["nng"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_nng")
            dpg.add_separator()
            
            dpg.add_input_text(label="R² Score", 
                               default_value=str(self.node_instance.params["r2_score"]),
                               tag=f"{self.INPUT_TAG}_{self.node_id}_r2_score",
                               readonly=True)
            dpg.add_button(label="Save Changes", callback=self.popup_callback)

    def popup_callback(self):
        self.node_instance.params["test_size"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_test_size")
        self.node_instance.params["nng"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_nng")
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")

    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_r2_score",
                      self.node_instance.params["r2_score"])

        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_test_size",
                      self.node_instance.params["test_size"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_nng",
                      self.node_instance.params["nng"])