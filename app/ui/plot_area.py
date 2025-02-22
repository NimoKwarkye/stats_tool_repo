import dearpygui.dearpygui as dpg
from app.utils.constants import PLOT_AREA_TAG, PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG

class PlotArea:
    def __init__(self):
        self.plot_tags = [PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG]

    def no_data_plot(self, parent: str):
        dpg.delete_item(parent + "_main")
        if dpg.does_item_exist(parent + "_main_fit"):
            dpg.delete_item(parent + "_main_fit")
        dpg.set_item_label(parent + "_x", "x")
        dpg.set_item_label(parent + "_y", "y")
        dpg.set_axis_limits(parent + "_x", 0, 1)  # lock axis limits so annotation is centered
        dpg.set_axis_limits(parent + "_y", 0, 1)
        dpg.add_plot_annotation(label="No Data Available", default_value=(0.5, 0.5), tag=parent + "_main", parent=parent)

    def scatter_plot(self, parent: str, node_params, plot_data):
        dpg.delete_item(parent + "_main")
        if dpg.does_item_exist(parent + "_main_fit"):
            dpg.delete_item(parent + "_main_fit")

        dpg.set_item_label(parent + "_x", node_params["xlabel"])
        dpg.set_item_label(parent + "_y", node_params["ylabel"])
        dpg.set_axis_limits(parent + "_y", min(plot_data["y"]), max(plot_data["y"]))
        dpg.set_axis_limits(parent + "_x", min(plot_data["x"]), max(plot_data["x"]))  # lock axis limits so annotation is centered

        dpg.add_scatter_series(plot_data["x"], plot_data["y"], label=node_params["title"],
                               tag=parent + "_main", parent=parent + "_y")

        if len(plot_data["trend_line"]) > 0:
            dpg.add_line_series(plot_data["trend_line"][0], plot_data["trend_line"][1],
                                label="fit", tag=parent + "_main_fit", parent=parent + "_y")
        dpg.fit_axis_data(parent + "_x")
        dpg.fit_axis_data(parent + "_y")

        dpg.set_axis_limits_auto(parent + "_x")
        dpg.set_axis_limits_auto(parent + "_y")

    def plot_themes(self):
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (244, 162, 97), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)

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
                        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag=plot_tag + "_x")
                        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag=plot_tag + "_y")
                        self.no_data_plot(plot_tag)
