import dearpygui.dearpygui as dpg
from app.ui.base_node_ui import BaseNodeUI


class LogisticRegressionNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()

    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("Logistic Regression Node")
            dpg.add_separator()
            dpg.add_combo(label="penaly", items=["l1", "l2", "elasticnet"],
                          default_value="l2", tag=f"{self.POP_UP_TAG}_penalty")
            dpg.add_checkbox(label="dual", default_value=False, tag=f"{self.POP_UP_TAG}_dual")
            dpg.add_input_float(label="tol", default_value=1e-4, tag=f"{self.POP_UP_TAG}_tol")
            dpg.add_input_float(label="C", default_value=1.0, tag=f"{self.POP_UP_TAG}_C")
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="fit intercept", default_value=True, tag=f"{self.POP_UP_TAG}_fit_intercept")
                dpg.add_input_float(label="intercept scaling", default_value=1, tag=f"{self.POP_UP_TAG}_intercept_scaling")
            dpg.add_combo(label="class weight", items=["balanced", "None"],
                          default_value="None", tag=f"{self.POP_UP_TAG}_class_weight")
            dpg.add_input_int(label="random state", default_value=0, tag=f"{self.POP_UP_TAG}_random_state")
            dpg.add_combo(label="solver", items=["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
                          default_value="lbfgs", tag=f"{self.POP_UP_TAG}_solver")
            dpg.add_input_int(label="max iter", default_value=100, tag=f"{self.POP_UP_TAG}_max_iter")
            dpg.add_checkbox(label="warm start", default_value=False, tag=f"{self.POP_UP_TAG}_warm_start")
            dpg.add_input_int(label="n jobs", default_value=1, tag=f"{self.POP_UP_TAG}_n_jobs",
                              min_value=1, min_clamped=True)
            dpg.add_input_float(label="l1 ratio", default_value=-1.0, tag=f"{self.POP_UP_TAG}_l1_ratio",
                                min_value=-1.0, max_value=1.0, min_clamped=True, max_clamped=True)
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["penalty"] = dpg.get_value(f"{self.POP_UP_TAG}_penalty")
        self.node_instance.params["dual"] = dpg.get_value(f"{self.POP_UP_TAG}_dual")
        self.node_instance.params["tol"] = dpg.get_value(f"{self.POP_UP_TAG}_tol")
        self.node_instance.params["C"] = dpg.get_value(f"{self.POP_UP_TAG}_C")
        self.node_instance.params["fit_intercept"] = dpg.get_value(f"{self.POP_UP_TAG}_fit_intercept")
        self.node_instance.params["intercept_scaling"] = dpg.get_value(f"{self.POP_UP_TAG}_intercept_scaling")

        cls_wgt = dpg.get_value(f"{self.POP_UP_TAG}_class_weight")
        self.node_instance.params["class_weight"] = None if cls_wgt == "None" else cls_wgt
        rnd_state = dpg.get_value(f"{self.POP_UP_TAG}_random_state")
        self.node_instance.params["random_state"] = None if rnd_state == 0 else rnd_state 
        self.node_instance.params["solver"] = dpg.get_value(f"{self.POP_UP_TAG}_solver")
        self.node_instance.params["max_iter"] = dpg.get_value(f"{self.POP_UP_TAG}_max_iter")
        self.node_instance.params["warm_start"] = dpg.get_value(f"{self.POP_UP_TAG}_warm_start")
        n_jobs = dpg.get_value(f"{self.POP_UP_TAG}_n_jobs")
        self.node_instance.params["n_jobs"] = None if n_jobs == 1 else n_jobs
        l1_ratio = dpg.get_value(f"{self.POP_UP_TAG}_l1_ratio")
        self.node_instance.params["l1_ratio"] = None if l1_ratio < 0.0 else l1_ratio

        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.POP_UP_TAG}_penalty", self.node_instance.params["penalty"])
        dpg.set_value(f"{self.POP_UP_TAG}_dual", self.node_instance.params["dual"])
        dpg.set_value(f"{self.POP_UP_TAG}_tol", self.node_instance.params["tol"])
        dpg.set_value(f"{self.POP_UP_TAG}_C", self.node_instance.params["C"])
        dpg.set_value(f"{self.POP_UP_TAG}_fit_intercept", self.node_instance.params["fit_intercept"])
        dpg.set_value(f"{self.POP_UP_TAG}_intercept_scaling", self.node_instance.params["intercept_scaling"])
        dpg.set_value(f"{self.POP_UP_TAG}_class_weight", self.node_instance.params["class_weight"])

        rnd_state = self.node_instance.params["random_state"]
        dpg.set_value(f"{self.POP_UP_TAG}_random_state", 0 if rnd_state is None else rnd_state)
        dpg.set_value(f"{self.POP_UP_TAG}_solver", self.node_instance.params["solver"])
        dpg.set_value(f"{self.POP_UP_TAG}_max_iter", self.node_instance.params["max_iter"])
        dpg.set_value(f"{self.POP_UP_TAG}_warm_start", self.node_instance.params["warm_start"])
        n_jobs = self.node_instance.params["n_jobs"]
        dpg.set_value(f"{self.POP_UP_TAG}_n_jobs", 1 if n_jobs is None else n_jobs)
        l1_ratio = self.node_instance.params["l1_ratio"]
        dpg.set_value(f"{self.POP_UP_TAG}_l1_ratio", -1.0 if l1_ratio is None else l1_ratio)
        