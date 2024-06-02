import dearpygui.dearpygui as dpg
import numpy as np
import constants


from dataclasses import dataclass

@dataclass
class Series_Data:
    xlabel : str = "x"
    ylabel : str = "y"
    x_data : np.ndarray = []
    y_data : np.ndarray = []
    color  : list = []
    title  : str = "graph"
    plot_type : str = "line"
    label : str = "line"
    tag = dpg.generate_uuid() 

class Plot_Series:
    def __init__(self, graph_data :Series_Data):
        self.graph_data = graph_data
    
    def __call__(self):
        with dpg.plot(parent=constants.PLOT_WINDOW):
            dpg.add_plot_axis(dpg.mvXAxis, label=self.graph_data.xlabel)
            dpg.add_plot_axis(dpg.mvYAxis, label=self.graph_data.ylabel)
            if self.graph_data.plot_type == "line":
                dpg.add_line_series(self.graph_data.x_data, self.graph_data.y_data, label=self.graph_data.label, tag=self.graph_data.tag)
            elif self.graph_data.plot_type == "scatter":
                dpg.add_scatter_series(self.graph_data.x_data, self.graph_data.y_data, label=self.graph_data.label, tag=self.graph_data.tag)

    def update(self, new_data):
        dpg.configure_item(self.graph_data.tag, x=new_data[0], y=new_data[1])


