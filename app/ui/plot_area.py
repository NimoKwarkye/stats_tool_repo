import dearpygui.dearpygui as dpg
from app.utils.constants import PLOT_AREA_TAG, PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG

class PlotArea:
    def __init__(self):
        self.plot_tags = [PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG]
        self.track_tags = {}
        for tag in self.plot_tags:
            self.track_tags[tag] = []

    
    def no_data_plot(self, parent: str):
        self.clear_plot(parent)
        plot_main_tag = parent + f"_main_{dpg.generate_uuid()}"
        self.track_tags[parent].append(plot_main_tag)
        dpg.set_item_label(parent + "_x", "x")
        dpg.set_item_label(parent + "_y", "y")
        dpg.set_axis_limits(parent + "_x", 0, 1)  # lock axis limits so annotation is centered
        dpg.set_axis_limits(parent + "_y", 0, 1)
        dpg.add_plot_annotation(label="No Data Available", default_value=(0.5, 0.5), tag=plot_main_tag, parent=parent)

    
    def scatter_plot(self, parent: str, node_params, plot_data):
        self.clear_plot(parent)
        
        plot_main_tag = parent + f"_main_{dpg.generate_uuid()}"
        plot_main_theme_tag = parent + f"_main_theme_{dpg.generate_uuid()}"
        self.track_tags[parent].append(plot_main_tag)
        self.track_tags[parent].append(plot_main_theme_tag)

        dpg.set_item_label(parent, node_params["title"])
        dpg.set_item_label(parent + "_x", node_params["xlabel"])
        dpg.set_item_label(parent + "_y", node_params["ylabel"])

        dpg.add_scatter_series(plot_data["x"], plot_data["y"], label=node_params["plot_label"],
                               tag=plot_main_tag, parent=parent + "_y")
        self.create_scatter_theme(plot_main_theme_tag, node_params["marker_color"], node_params["marker_style"])
        dpg.bind_item_theme(plot_main_tag, plot_main_theme_tag)

        if len(plot_data["trend_line"]) > 0:
            fit_tag = parent + f"_fit_{dpg.generate_uuid()}"
            fit_theme_tag = parent + f"_fit_theme_{dpg.generate_uuid()}"
            self.track_tags[parent].append(fit_tag)
            self.track_tags[parent].append(fit_theme_tag)
            
            dpg.add_line_series(plot_data["trend_line"][0], plot_data["trend_line"][1],
                                label=node_params["fit_label"], tag=fit_tag, parent=parent + "_y")
            self.create_line_theme(fit_theme_tag, node_params["line_color"])
            dpg.bind_item_theme(fit_tag, fit_theme_tag)

        dpg.fit_axis_data(parent + "_x")
        dpg.fit_axis_data(parent + "_y")

        dpg.set_axis_limits_auto(parent + "_x")
        dpg.set_axis_limits_auto(parent + "_y")


    def heatmap_plot(self, parent: str, node_params, plot_data):
        self.clear_plot(parent)
        
        plot_main_tag = parent + f"_main_{dpg.generate_uuid()}"
        self.track_tags[parent].append(plot_main_tag)

        dpg.set_item_label(parent, node_params["title"])
        dpg.set_item_label(parent + "_x", node_params["xlabel"])
        dpg.set_item_label(parent + "_y", node_params["ylabel"])

        dpg.add_heat_series(plot_data["data"], rows=plot_data["rows"], cols=plot_data["cols"], 
                            tag=plot_main_tag, parent=parent + "_y", bounds_min=node_params["bounds_min"], 
                            bounds_max=node_params["bounds_max"], format="", scale_min=plot_data["scale_min"],
                            scale_max=plot_data["scale_max"])
        dpg.bind_colormap(parent, node_params["colormap"])

        dpg.fit_axis_data(parent + "_x")
        dpg.fit_axis_data(parent + "_y")

    
    def clear_plot(self, parent: str):
        for item_id in self.track_tags[parent]:
            dpg.delete_item(item_id)
        self.track_tags[parent] = []

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

    
    def plot_setup(self):
        with dpg.window(tag=PLOT_AREA_TAG,
                        label="Plots",
                        no_close=True,
                        no_collapse=True,
                        no_scrollbar=True,
                        no_scroll_with_mouse=True):
            with dpg.subplots(rows=2, columns=3, height=-1, width=-1):
                for plot_tag in self.plot_tags:
                    with dpg.plot(label=f"Plot {self.plot_tags.index(plot_tag) + 1}", height=-1, width=-1, tag=plot_tag):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag=plot_tag + "_x")
                        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag=plot_tag + "_y")
                        self.no_data_plot(plot_tag)
