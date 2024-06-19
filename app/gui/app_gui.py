import dearpygui.dearpygui as dpg

from app import constants
from app.algorithms import (pca)
from sklearn import datasets
from app.plot import app_graph as gph
import numpy as np
from app.gui import pca_ui

class App_Ui:
    def __init__(self):
        self.primar_window = None
        self.graph = None
        
    
    def __call__(self):
        with dpg.window(no_scrollbar=True) as self.primar_window:
            self.main_menubar()
            with dpg.tab_bar(tag=constants.PRIMARY_TAB):
                with dpg.tab(label="Home"):
                    pass
                
                            
        dpg.set_primary_window(self.primar_window, True)
    
    def pca_callback(self):
        with dpg.window(label="PCA Parameters Window", height=500, width=300):
            pass

    def pca_exe_callback(self, raw_data:np.ndarray, input_data: pca.PCA_Input, targets:list):
        pca_instance = pca.PCA(input_data, raw_data)
        results = pca_instance()
        self.graph.init_plot([list(results[:, 0]), list(results[:, 1]), targets], gph.pca_plotter)
        

    def main_menubar(self):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New")
                dpg.add_menu_item(label="Open")
            
            with dpg.menu(label="Edit"):
                dpg.add_menu_item(label="Something")
                dpg.add_menu_item(label="Preferences")
            
            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="PCA", callback=pca_ui.show)
                dpg.add_menu_item(label="Factor Analysis")
                dpg.add_menu_item(label="Parallel Factor Analysis")
        
    

   


