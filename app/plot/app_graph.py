import dearpygui.dearpygui as dpg
import numpy as np
from app import constants


from dataclasses import dataclass

@dataclass
class Series_Data:
    xlabel : str = "x"
    ylabel : str = "y"
    color  : list = None
    title  : str = "graph"
    plot_type : str = "line"
    label : str = "line"
    tag :  str = "pca_plot"


def pca_plotter(x_data:list, y_data:list, targets : list=None):
    if targets is None:
        dpg.add_scatter_series(x_data, y_data, parent=constants.YAXIS_1)
    else:
        if len(targets) == len(x_data):
            colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)]
            split_data = {}
            unique_targets = set(targets)
            for tg in unique_targets:
                split_data[tg] = [[], []]

            for idx, tg in enumerate(targets):
                split_data[tg][0].append(x_data[idx])
                split_data[tg][1].append(y_data[idx])
            for tg_data in split_data:
                dpg.add_scatter_series(split_data[tg_data][0], split_data[tg_data][1], parent=constants.YAXIS_1)

        else:
            dpg.add_scatter_series(x_data, y_data, parent=constants.YAXIS_1)

class Plot_Series:
    def __init__(self, graph_data :Series_Data):
        self.graph_data = graph_data
        self.data_ploted = False
    def __call__(self):
        with dpg.plot(height=-1, width=-1):
            dpg.add_plot_axis(dpg.mvXAxis, label=self.graph_data.xlabel, tag=constants.XAXIS_1)
            dpg.add_plot_axis(dpg.mvYAxis, label=self.graph_data.ylabel, tag=constants.YAXIS_1)
            dpg.set_axis_limits(constants.XAXIS_1, 0, 1) # lock axis limits so annotation is centered
            dpg.set_axis_limits(constants.YAXIS_1, 0, 1)
            dpg.add_plot_annotation(label="No Data Available", default_value=(0.5, 0.5), tag=constants.ANNOTATION_PLOT)
            

    def update(self, new_data):
        dpg.configure_item(self.graph_data.tag, x=new_data[0], y=new_data[1])
    
    def init_plot(self, new_data:list, plot_function):
        new_data.append(None)
        self.clear_plot()
        plot_function(new_data[0], new_data[1], new_data[2])
        self.data_ploted = True
        dpg.set_axis_limits_auto(constants.XAXIS_1) # unlock axis limits
        dpg.set_axis_limits_auto(constants.YAXIS_1)
        dpg.hide_item(constants.ANNOTATION_PLOT)
    
    def clear_plot(self):
        if self.data_ploted:
            dpg.delete_item(constants.YAXIS_1, children_only=True)
            dpg.set_axis_limits(constants.YAXIS_1, 0, 1) 
            dpg.set_axis_limits(constants.XAXIS_1, 0, 1)
            dpg.show_item(constants.ANNOTATION_PLOT)
            self.data_ploted = False

def plot_correlation_map(parent, data:np.ndarray, features:list[str]):
    correlation_matrix = np.corrcoef(data, rowvar=False)
    axis_vals = np.linspace(0.0, 1.0, len(features), endpoint=False)
    axis_vals += (axis_vals[1] - axis_vals[0])/2.0
    labels = tuple([(feature, i) for feature, i in zip(features, axis_vals)])

    with dpg.plot(label="Correlation Matrix", height=400, width=-1,  parent=parent):
        dpg.bind_colormap(dpg.last_item(), dpg.mvPlotColormap_Jet)
        
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, lock_min=True, lock_max=True)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, lock_min=True, lock_max=True)

        values = list(correlation_matrix.flatten())
        heat_series = dpg.add_heat_series(values, len(features), len(features), 
                                            format="%.2f", 
                                            parent=y_axis,
                                            scale_min=-1.0,
                                            scale_max=1.0)

        dpg.set_axis_ticks(x_axis, labels)
        dpg.set_axis_ticks(y_axis, labels)
