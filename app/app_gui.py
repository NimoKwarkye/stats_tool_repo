import dearpygui.dearpygui as dpg
from itertools import chain
import constants
import algorithms as alg
from sklearn import datasets
import app_graph as gph

class App_Ui:
    def __init__(self):
        self.primar_window = None
        self.graph = None
        
    
    def __call__(self):
        with dpg.window(no_scrollbar=True) as self.primar_window:
            self.main_menubar()
            with dpg.table(header_row=False, resizable=True):
                dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window() as child_window_1:
                        dpg.add_text("Child Window 1")
                        dpg.add_button(label="PCA", callback= self.pca_callback)
                    with dpg.group():
                        with dpg.child_window(height=500, tag=constants.PLOT_WINDOW) as child_window_2:
                            data_series = gph.Series_Data(xlabel="PC1", ylabel="PC2", plot_type="scatter")
                            self.graph = gph.Plot_Series(data_series)
                            self.graph()
                        self.adjustable_separator(child_window_2)
                        with dpg.child_window():
                            dpg.add_text("Child Window 3")
                    
        dpg.set_primary_window(self.primar_window, True)
    
    def pca_callback(self):
        pca_data = alg.PCA_Input(n_components=2)
        iris = datasets.load_iris()
        X = iris.data
        pca_instance = alg.PCA(pca_data, X)
        results = pca_instance()
        self.graph.init_plot([list(results[:, 0]), list(results[:, 1]), list(iris.target)], gph.pca_plotter)


    def main_menubar(self):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New")
                dpg.add_menu_item(label="Open")
            
            with dpg.menu(label="Edit"):
                dpg.add_menu_item(label="Something")
                dpg.add_menu_item(label="Preferences")
            
            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="PCA")
                dpg.add_menu_item(label="Factor Analysis")
                dpg.add_menu_item(label="Parallel Factor Analysis")
        
    def adjustable_separator(self, child_window, width=3840, height=2, colour=(255, 255, 255, 50)):
        with dpg.texture_registry():
            data = list(chain.from_iterable([[c / 255 for c in colour] for _ in range(width*height)]))
            separator_texture = dpg.add_static_texture(width=width, height=height, default_value=data)
        separator = dpg.add_image(separator_texture)
        def clicked_callback():
            while dpg.is_mouse_button_down(0):
                y_pos = dpg.get_mouse_pos()[1]
                dpg.split_frame(delay=10)
                y_delta = y_pos - dpg.get_mouse_pos()[1]
                height = dpg.get_item_height(child_window) - y_delta
                if height < 1: height = 1
                dpg.configure_item(child_window, height=height)
        with dpg.item_handler_registry() as item_handler:
            dpg.add_item_clicked_handler(callback=clicked_callback)
        dpg.bind_item_handler_registry(item=separator, handler_registry=item_handler)

   


