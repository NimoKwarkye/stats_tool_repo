import dearpygui.dearpygui as dpg
import numpy as np
from app.utils.constants import PLOT_AREA_TAG, PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG


class BasePlot:
    def __init__(self):
        self.plot_tags = [PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG]
        self.track_tags = {}
        for tag in self.plot_tags:
            self.track_tags[tag] = []
    
    def clear_plot_region(self, plot_region: str):
        dpg.delete_item(plot_region, children_only=True)
        for item_id in self.track_tags[plot_region]:
            if dpg.does_item_exist(item_id):
                dpg.delete_item(item_id)
        self.track_tags[plot_region] = []
    
    def create_line_theme(self, tag: str, color: tuple[int, int, int, int]):
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, color, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)
    
    def create_scatter_theme(self, tag: str, color: tuple[int, int, int, int], marker_style: int = dpg.mvPlotMarker_Circle):
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvScatterSeries):
                dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, color, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, color, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, marker_style, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)
    
    def plot(self, node_params, plot_data):
        raise NotImplementedError


class ScatterPlot(BasePlot):

    def plot(self, node_params, plot_data):
        plot_region = node_params["region"]
        self.clear_plot_region(plot_region)

        plot_main_tag = plot_region + f"_main_{dpg.generate_uuid()}"
        plot_main_theme_tag = plot_region + f"_main_theme_{dpg.generate_uuid()}"
        self.track_tags[plot_region].append(plot_main_tag)
        self.track_tags[plot_region].append(plot_main_theme_tag)

        with dpg.plot(label=f"Plot {self.plot_tags.index(node_params['region']) + 1}", 
                      height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_main_tag + "_x")
            dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_main_tag + "_y")
            dpg.add_scatter_series(plot_data["x"], plot_data["y"], label=node_params["plot_label"],
                                   tag=plot_main_tag + "scatter", parent=plot_main_tag + "_y")
            self.create_scatter_theme(plot_main_theme_tag, node_params["marker_color"], node_params["marker_style"])
            dpg.bind_item_theme(plot_main_tag + "scatter", plot_main_theme_tag)

            if len(plot_data["trend_line"]) > 0:
                fit_tag = plot_region + f"_fit_{dpg.generate_uuid()}"
                fit_theme_tag = plot_region + f"_fit_theme_{dpg.generate_uuid()}"
                self.track_tags[plot_region].append(fit_tag)
                self.track_tags[plot_region].append(fit_theme_tag)
                
                dpg.add_line_series(plot_data["trend_line"][0], plot_data["trend_line"][1],
                                    label=node_params["fit_label"], tag=fit_tag, parent=plot_main_tag + "_y")
                self.create_line_theme(fit_theme_tag, node_params["line_color"])
                dpg.bind_item_theme(fit_tag, fit_theme_tag)
        
        dpg.fit_axis_data(plot_main_tag + "_x")
        dpg.fit_axis_data(plot_main_tag + "_y")
        dpg.set_axis_limits_auto(plot_main_tag + "_x")
        dpg.set_axis_limits_auto(plot_main_tag + "_y")


class HeatmapPlot(BasePlot):
    
    def plot(self, node_params, plot_data):
        plot_region = node_params["region"]
        self.clear_plot_region(plot_region)

        plot_main_tag = plot_region + f"_main_{dpg.generate_uuid()}"
        self.track_tags[plot_region].append(plot_main_tag)

        with dpg.plot(label=f"Plot {self.plot_tags.index(node_params['region']) + 1}", 
                      height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_main_tag + "_x")
            dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_main_tag + "_y")
            dpg.add_heat_series(plot_data["data"], rows=plot_data["rows"], cols=plot_data["cols"], 
                                tag=plot_main_tag + "heat", parent=plot_main_tag + "_y", bounds_min=node_params["bounds_min"], 
                                bounds_max=node_params["bounds_max"], format="", scale_min=plot_data["scale_min"],
                                scale_max=plot_data["scale_max"])
            dpg.bind_colormap(plot_region, node_params["colormap"])
        
        dpg.fit_axis_data(plot_main_tag + "_x")
        dpg.fit_axis_data(plot_main_tag + "_y")


class PairGridPlot(BasePlot):

    def plot(self, node_params, plot_data):
        data = np.array(plot_data["data"])
        if data.ndim == 1:
            return
        n_features = min(data.shape[1], 10)
        if node_params["labels"] is None:
            labels = [f"Var {i+1}" for i in range(n_features)]
        else:
            labels = node_params["labels"]
        
        self.clear_plot_region(node_params["region"])
        with dpg.subplots(rows=n_features, columns=n_features, parent=node_params["region"], height=-1, width=-1):
            for i in range(n_features):
                for j in range(n_features):
                    cell_tag = f"pairgrid_{i}_{j}_{dpg.generate_uuid()}"
                    with dpg.plot(label="", height=150, width=150, tag=cell_tag):
                        x_axis_tag = cell_tag + "_x"
                        y_axis_tag = cell_tag + "_y"
                        dpg.add_plot_axis(dpg.mvXAxis, label=labels[j], tag=x_axis_tag)
                        dpg.add_plot_axis(dpg.mvYAxis, label=labels[i], tag=y_axis_tag)
                        
                        if i == j:
                            dpg.add_plot_annotation(label=labels[i], default_value=(0.5, 0.5), parent=cell_tag)
                        else:
                            x = data[:, j].tolist()
                            y = data[:, i].tolist()
                            dpg.add_scatter_series(x, y, label=f"{labels[j]} vs {labels[i]}", parent=y_axis_tag)
                            
                        dpg.fit_axis_data(x_axis_tag)
                        dpg.fit_axis_data(y_axis_tag)

class NoDataPlot(BasePlot):
    
    def plot(self, node_params, plot_data=None):
        plot_region = node_params["region"]
        self.clear_plot_region(plot_region)
        plot_main_tag = plot_region + f"_main_{dpg.generate_uuid()}"
        self.track_tags[plot_region].append(plot_main_tag)
        with dpg.plot(label=f"Plot {self.plot_tags.index(node_params['region']) + 1}", 
                      height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_region + "_x")
            dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_region + "_y")
            dpg.add_plot_annotation(label="No Data Available", default_value=(0.5, 0.5), 
                                    parent=plot_main_tag)
        dpg.fit_axis_data(plot_region + "_x")
        dpg.fit_axis_data(plot_region + "_y")

class PlotManager:
    def __init__(self):
        self.plot_types = {
            "scatter": ScatterPlot(),
            "heatmap": HeatmapPlot(),
            "pairgrid": PairGridPlot(),
            "no_data": NoDataPlot()
        }

    def plot(self, node_params, plot_data):
        self.plot_types[node_params["plot_type"]].plot(node_params, plot_data)

class PlotArea:
    def __init__(self):
        self.plot_manager = PlotManager()
        self.plot_tags = [PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG]
        self.nrows = 2
        self.ncols = 3
    
    def plot_setup(self):
        with dpg.window(tag=PLOT_AREA_TAG,
                        label="Plots",
                        no_close=True,
                        no_collapse=True,
                        no_scrollbar=True,
                        no_scroll_with_mouse=True):
            for row in range(self.nrows):
                if row < self.nrows - 1:
                    with dpg.child_window(width=-1, height=200, resizable_y=True, autosize_x=True, autosize_y=True, border=False):
                        with dpg.table(header_row=False, resizable=True, borders_innerH=True, width=-1):
                            for col in range(self.ncols):
                                dpg.add_table_column(width=-1)
                            with dpg.table_row(height=-1):
                                for col in range(self.ncols):
                                    child_tag = self.plot_tags[row*self.ncols + col]
                                    with dpg.child_window(tag=child_tag,
                                                    width=-1,
                                                    height=-1,       # initial height is automatic
                                                    autosize_x=True,
                                                    autosize_y=True,
                                                    resizable_x=False,
                                                    resizable_y=False, border=False):
                                        plot_data = {"plot_type": "no_data", "region": child_tag,
                                                     "xlabel": "X-axis", "ylabel": "Y-axis"}
                                        self.plot_manager.plot(plot_data, None)
                else:
                    with dpg.child_window(width=-1, height=200, resizable_y=False, autosize_x=True, autosize_y=True, border=False):
                        with dpg.table(header_row=False, resizable=True, borders_innerH=True, width=-1):
                            for col in range(self.ncols):
                                dpg.add_table_column(width=-1)
                            with dpg.table_row(height=-1):
                                for col in range(self.ncols):
                                    child_tag = self.plot_tags[row*self.ncols + col]
                                    with dpg.child_window(tag=child_tag,
                                                    width=-1,
                                                    height=-1,       # initial height is automatic
                                                    autosize_x=True,
                                                    autosize_y=True,
                                                    resizable_x=False,
                                                    resizable_y=False, border=False):
                                        plot_data = {"plot_type": "no_data", "region": child_tag,
                                                     "xlabel": "X-axis", "ylabel": "Y-axis"}
                                        self.plot_manager.plot(plot_data, None)

    
