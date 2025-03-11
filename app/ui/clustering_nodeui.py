import dearpygui.dearpygui as dpg
from app.ui.base_node_ui import BaseNodeUI


class KmeansNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("KMeans Clustering Node")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="clusters count", 
                                default_value=self.node_instance.params["n_clusters"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_n_clusters", 
                                min_value=1, max_value=10,
                                max_clamped=True, min_clamped=True)
                dpg.add_checkbox(label="copy data",
                            default_value=self.node_instance.params["copy_x"],
                            tag=f"{self.INPUT_TAG}_{self.node_id}_copy_x")
            dpg.add_separator()    
            dpg.add_combo(label="init", items=["k-means++", "random"],
                          default_value=self.node_instance.params["init"],
                          tag=f"{self.INPUT_TAG}_{self.node_id}_init")
            dpg.add_input_int(label="init count",
                              tag=f"{self.INPUT_TAG}_{self.node_id}_n_init", 
                              min_value=0, min_clamped=True)
            dpg.add_input_int(label="max iter",
                              default_value=self.node_instance.params["max_iter"],
                              tag=f"{self.INPUT_TAG}_{self.node_id}_max_iter", 
                              min_value=1, min_clamped=True)
            dpg.add_input_float(label="tol",
                                default_value=self.node_instance.params["tol"],
                                tag=f"{self.INPUT_TAG}_{self.node_id}_tol", 
                                min_value=0.0, min_clamped=True)
            
            dpg.add_input_int(label="random state",
                              tag=f"{self.INPUT_TAG}_{self.node_id}_random_state", 
                              min_value=0, min_clamped=True)
            dpg.add_combo(label="algorithm", items=["lloyd", "elkan"],
                          default_value=self.node_instance.params["algorithm"],
                          tag=f"{self.INPUT_TAG}_{self.node_id}_algorithm")
            dpg.add_separator()
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["n_clusters"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_n_clusters")
        self.node_instance.params["copy_x"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_copy_x")
        self.node_instance.params["init"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_init")
        n_init = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_n_init")
        if n_init == 0:
            self.node_instance.params["n_init"] = "auto"
        else:
            self.node_instance.params["n_init"] = n_init
        self.node_instance.params["max_iter"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_max_iter")
        self.node_instance.params["tol"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_tol")
        rnd_state = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_random_state")
        if rnd_state == 0:
            self.node_instance.params["random_state"] = None
        else:
            self.node_instance.params["random_state"] = rnd_state
        self.node_instance.params["algorithm"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_algorithm")
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_clusters",
                      self.node_instance.params["n_clusters"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_copy_x",
                      self.node_instance.params["copy_x"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_init",
                      self.node_instance.params["init"])
        
        if self.node_instance.params["n_init"] == "auto":
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_init", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_n_init", self.node_instance.params["n_init"])
        
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_max_iter",
                      self.node_instance.params["max_iter"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_tol",
                      self.node_instance.params["tol"])
        if self.node_instance.params["random_state"] is None:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state", 0)
        else:
            dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_random_state", self.node_instance.params["random_state"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_algorithm",
                      self.node_instance.params["algorithm"])


class DBSCANNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("DBSCAN Clustering Node")
            dpg.add_separator()
            dpg.add_input_float(label="eps", 
                            default_value=self.node_instance.params["eps"],
                            tag=f"{self.INPUT_TAG}_{self.node_id}_eps", 
                            min_value=0.0, max_value=10.0,
                            max_clamped=True, min_clamped=True)
            dpg.add_input_int(label="min samples",
                        default_value=self.node_instance.params["min_samples"],
                        tag=f"{self.INPUT_TAG}_{self.node_id}_min_samples", 
                        min_value=1, max_value=10,
                        max_clamped=True, min_clamped=True)
            dpg.add_combo(label="metric", items=["euclidean", "manhattan", "chebyshev", "l1", "l2"],
                          default_value=self.node_instance.params["metric"],
                          tag=f"{self.INPUT_TAG}_{self.node_id}_metric")
            dpg.add_combo(label="algorithm", items=["auto", "ball_tree", "kd_tree", "brute"],
                          default_value=self.node_instance.params["algorithm"],
                          tag=f"{self.INPUT_TAG}_{self.node_id}_algorithm")
            dpg.add_separator()
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["eps"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_eps")
        self.node_instance.params["min_samples"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_min_samples")
        self.node_instance.params["metric"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_metric")
        self.node_instance.params["algorithm"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_algorithm")
        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_eps",
                      self.node_instance.params["eps"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_min_samples",
                      self.node_instance.params["min_samples"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_metric",
                      self.node_instance.params["metric"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_algorithm",
                      self.node_instance.params["algorithm"])
    
            
            