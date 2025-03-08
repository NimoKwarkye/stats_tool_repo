import dearpygui.dearpygui as dpg
from app.ui.base_node_ui import BaseNodeUI



class PCANodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("PCA Node")
            dpg.add_separator()
            dpg.add_input_int(label="components count", 
                              default_value=self.node_instance.params["n_components"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_n_components", 
                              min_value=1, max_value=10,
                              max_clamped=True, min_clamped=True)
            dpg.add_checkbox(label="copy data", 
                            default_value=self.node_instance.params["copy_data"],
                            tag=f"{self.INPUT_TAG}_{self.node_id}_copy_data")
            dpg.add_checkbox(label="apply whiten", 
                            default_value=self.node_instance.params["whiten"],
                            tag=f"{self.INPUT_TAG}_{self.node_id}_whiten")
            dpg.add_combo(items=["auto", "full", "covariance_eigh", "arpack", "randomized"], 
                                label="svd solver", 
                               default_value=self.node_instance.params["svd_solver"],
                               tag=f"{self.INPUT_TAG}_{self.node_id}_svd_solver")
            dpg.add_input_float(label="tol", 
                                default_value=self.node_instance.params["tol"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_tol")
            dpg.add_input_int(label="iterated power", 
                               min_value=0, min_clamped=True,
                               tag=f"{self.INPUT_TAG}_{self.node_id}_iterated_power")
            dpg.add_input_int(label="random state",
                              min_value=0, min_clamped=True, 
                              tag=f"{self.INPUT_TAG}_{self.node_id}_random_state")
            dpg.add_combo(items=["auto", "QR", "LU", "none"],
                                label="power iteration normalizer", 
                               default_value=self.node_instance.params["power_iteration_normalizer"],
                               tag=f"{self.INPUT_TAG}_{self.node_id}_power_iteration_normalizer")
            dpg.add_input_int(label="oversamples count",
                                min_value=10, min_clamped=True, 
                              default_value=self.node_instance.params["n_over_samples"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_n_over_samples")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["n_components"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_n_components")
        self.node_instance.params["copy_data"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_copy_data")
        self.node_instance.params["whiten"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_whiten")
        self.node_instance.params["svd_solver"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_svd_solver")
        self.node_instance.params["tol"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_tol")
        self.node_instance.params["iterated_power"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_iterated_power")
        self.node_instance.params["power_iteration_normalizer"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_power_iteration_normalizer")
        self.node_instance.params["n_over_samples"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_n_over_samples")
        rnd_state = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_random_state")
        if rnd_state == 0:
            self.node_instance.params["random_state"] = None
        else:
            self.node_instance.params["random_state"] = rnd_state
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_components",
                      self.node_instance.params["n_components"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_copy_data",
                      self.node_instance.params["copy_data"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_whiten",
                      self.node_instance.params["whiten"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_svd_solver",
                      self.node_instance.params["svd_solver"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_tol",
                      self.node_instance.params["tol"])
        
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_power_iteration_normalizer",
                      self.node_instance.params["power_iteration_normalizer"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_over_samples",
                      self.node_instance.params["n_over_samples"])
        if self.node_instance.params["random_state"] is None:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state",
                        self.node_instance.params["random_state"])
            
        if self.node_instance.params["iterated_power"] == "auto":
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_iterated_power", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_iterated_power",
                          self.node_instance.params["iterated_power"])


class NMFNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("NMF Node")
            dpg.add_separator()
            dpg.add_input_int(label="components count", 
                              default_value=self.node_instance.params["n_components"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_n_components", 
                              min_value=1, max_value=10,
                              max_clamped=True, min_clamped=True)
            dpg.add_combo(label="init", 
                          items=["none", "random", "nndsvd", "nndsvda", "nndsvdar", "custom"],
                          default_value="none",
                          tag=f"{self.INPUT_TAG}_{self.node_id}_init")
            dpg.add_combo(label="solver",
                          items=["cd", "mu"],
                          default_value="cd",
                          tag=f"{self.INPUT_TAG}_{self.node_id}_solver")
            dpg.add_input_float(label="tol", 
                                default_value=self.node_instance.params["tol"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_tol")
            dpg.add_input_int(label="max iter",
                              default_value=self.node_instance.params["max_iter"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_max_iter")
            dpg.add_combo(label="beta loss",
                          items=["frobenius", "kullback-leibler", "itakura-saito"],
                          default_value="frobenius",
                          tag=f"{self.INPUT_TAG}_{self.node_id}_beta_loss")
            dpg.add_input_int(label="random state",
                              min_value=0, min_clamped=True, 
                              tag=f"{self.INPUT_TAG}_{self.node_id}_random_state")
            dpg.add_input_float(label="alpha W", 
                                default_value=self.node_instance.params["alpha_W"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_alpha_W")
            dpg.add_input_float(label="alpha H",
                              default_value=0.0,
                              tag=f"{self.INPUT_TAG}_{self.node_id}_alpha_H")
            dpg.add_input_float(label="l1 ratio", 
                                default_value=0.0,
                                tag=f"{self.INPUT_TAG}_{self.node_id}_l1_ratio")
            dpg.add_checkbox(label="shuffle", 
                            default_value=False,
                            tag=f"{self.INPUT_TAG}_{self.node_id}_shuffle")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)

    def popup_callback(self):
        n_components = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_n_components")
        if n_components == 0:
            self.node_instance.params["n_components"] = "auto"
        else:
            self.node_instance.params["n_components"] = n_components
        
        init = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_init")
        if init == "none":
            self.node_instance.params["init"] = None
        else:
            self.node_instance.params["init"] = init
        self.node_instance.params["solver"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_solver")
        self.node_instance.params["tol"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_tol")
        self.node_instance.params["max_iter"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_max_iter")
        self.node_instance.params["beta_loss"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_beta_loss")
        rnd_state = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_random_state")
        if rnd_state == 0:
            self.node_instance.params["random_state"] = None
        else:
            self.node_instance.params["random_state"] = rnd_state
        self.node_instance.params["alpha_W"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_alpha_W")
        self.node_instance.params["alpha_H"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_alpha_H")
        self.node_instance.params["l1_ratio"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_l1_ratio")
        self.node_instance.params["shuffle"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_shuffle")
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")

    def update_ui(self):
        n_components = self.node_instance.params["n_components"]
        if n_components == "auto":
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_components", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_components", n_components)
        
        init = self.node_instance.params["init"]
        if init is None:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_init", "none")
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_init", init)
        
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_solver", self.node_instance.params["solver"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_tol", self.node_instance.params["tol"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_max_iter", self.node_instance.params["max_iter"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_beta_loss", self.node_instance.params["beta_loss"])
        
        if self.node_instance.params["random_state"] is None:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state", self.node_instance.params["random_state"])
        
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_alpha_W", self.node_instance.params["alpha_W"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_alpha_H", self.node_instance.params["alpha_H"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_l1_ratio", self.node_instance.params["l1_ratio"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_shuffle", self.node_instance.params["shuffle"])


