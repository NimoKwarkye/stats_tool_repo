import dearpygui.dearpygui as dpg
import numpy as np
from app.utils.constants import PLOT_AREA_TAG, PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG
import colorsys

class BasePlot:
    def __init__(self):
        self.plot_tags = [PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG]
        self.track_tags = {}
        for tag in self.plot_tags:
            self.track_tags[tag] = []
        self.colors = self.generate_30_rgba()
    
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
        adjusted_color = [col for col in color]
        adjusted_color[-1] = 150
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvScatterSeries):
                dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, adjusted_color, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, color, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, marker_style, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)
    
    def create_histogram_theme(self, tag: str, color: tuple[int, int, int, int]):
        adjusted_color = [col for col in color]
        adjusted_color[-1] = 120
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvHistogramSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Fill, tuple(adjusted_color), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_Line, color, category=dpg.mvThemeCat_Plots)
        
    
    def generate_marker_colors(self, num_colors=30):
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            # High saturation and brightness for contrast on dark background
            saturation = 0.9
            value = 0.95
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            # Convert to 0-255 integer values and full alpha (255)
            colors.append((int(r * 255), int(g * 255), int(b * 255), 255))
        return colors
    def generate_30_rgba(self):
        # Begin with primary colors:
        # Red, Green, Blue, Cyan, Magenta, Yellow, and White (in place of Black)
        primary_colors = [
            (255, 0, 0, 255),    # Red
            (0, 255, 0, 255),    # Green
            (0, 0, 255, 255),    # Blue
            (0, 255, 255, 255),  # Cyan
            (255, 0, 255, 255),  # Magenta
            (255, 255, 0, 255),  # Yellow
            (255, 255, 255, 255) # White
        ]
        
        total_colors = 30
        remaining = total_colors - len(primary_colors)  # 23 additional colors
        
        additional_colors = []
        # Generate additional colors with high saturation and brightness.
        for i in range(remaining):
            hue = i / remaining  # even spacing across 0-1
            saturation = 0.9
            value = 0.95
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            rgba = (int(r * 255), int(g * 255), int(b * 255), 255)
            additional_colors.append(rgba)
        
        return primary_colors + additional_colors
    
    def plot(self, node_params, plot_data):
        raise NotImplementedError


class ScatterPlot(BasePlot):

    def plot(self, node_params, plot_data):
        plot_region = node_params["region"]
        self.clear_plot_region(plot_region)
        if plot_data["y"].ndim == 1 or plot_data["y"].shape[-1] == 1:
            y_data = list(plot_data["y"].flatten())
            data_dict = {}
            if plot_data["target_label"] is not None and \
                plot_data["target_label"].shape[0] == plot_data["y"].shape[0]:
                unique_labels = np.unique(plot_data["target_label"])
                for label in unique_labels:
                    indices = [i for i, l in enumerate(plot_data["target_label"]) if l == label]
    
                    y_values = [y_data[i] for i in indices]
                    x_values = [plot_data["x"][i] for i in indices]
                    
                    data_dict[f"{label}"] = [ x_values, y_values]
            else:
                data_dict[plot_data["plot_label"][0]] = [plot_data["x"], y_data]
                

                
            plot_main_tag = plot_region + f"_main_{dpg.generate_uuid()}"
            plot_main_theme_tag = plot_region + f"_main_theme_{dpg.generate_uuid()}"
            self.track_tags[plot_region].append(plot_main_tag)

            with dpg.plot(label=f"{node_params['title']}", 
                        height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_main_tag + "_x")
                dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_main_tag + "_y")
                for idx, label in enumerate(data_dict.keys()):
                    this_plot_tag = plot_main_tag + f"scatter{label}_{idx}"
                    dpg.add_scatter_series(data_dict[label][0], data_dict[label][0], label=label,
                                        tag=this_plot_tag, parent=plot_main_tag + "_y")
                    this_theme_tag = plot_main_theme_tag + f"_{label}_{idx}"
                    self.create_scatter_theme(this_theme_tag, self.colors[idx%30], node_params["marker_style"])
                    dpg.bind_item_theme(this_plot_tag, this_theme_tag)
                    self.track_tags[plot_region].append(this_theme_tag)

                
        else:
            features = plot_data["y"].shape[1]
            plot_main_tag = plot_region + f"_main_{dpg.generate_uuid()}"
            self.track_tags[plot_region].append(plot_main_tag)
            data_dict = {}
            use_target_labels = False
            if plot_data["target_label"] is not None and \
                plot_data["target_label"].shape[0] == plot_data["y"].shape[0]:
                unique_labels = np.unique(plot_data["target_label"])
                use_target_labels = True
                for label in unique_labels:
                    indices = [i for i, l in enumerate(plot_data["target_label"]) if l == label]
                    y_values = plot_data["y"][indices, :]
                    x_values = [plot_data["x"][i] for i in indices]
                    data_dict[f"{label}"] = [x_values, y_values]
            else:
                for i in range(features):
                    data_dict[plot_data["plot_label"][i]] = [plot_data["x"], plot_data["y"][:, i]]

            
            with dpg.plot(label=f"{node_params['title']}",
                          height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_main_tag + "_x")
                dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_main_tag + "_y")
                for idx, label in enumerate(data_dict.keys()):
                    y_data = []
                    x_data = []
                    this_plot_tag = plot_main_tag + f"scatter{label}_{idx}"
                    if use_target_labels:
                        for ft in range(features):
                            y_data += data_dict[label][1][:, ft].tolist()
                            x_data += data_dict[label][0]
                    else:
                        y_data = list(data_dict[label][1])
                        x_data = list(data_dict[label][0])
                    dpg.add_scatter_series(x_data, y_data, 
                                        label=label, tag=this_plot_tag, 
                                        parent=plot_main_tag + "_y")
                    this_theme_tag = plot_main_tag + f"_theme_{label}_{idx}"
                    self.create_scatter_theme(this_theme_tag, self.colors[idx%30], node_params["marker_style"])
                    dpg.bind_item_theme(this_plot_tag, this_theme_tag)
                    self.track_tags[plot_region].append(this_theme_tag)
                   
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

        with dpg.plot(label=f"{node_params['title']}", 
                      height=-1, width=-1, parent=plot_region, tag=plot_main_tag):   
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label=node_params["xlabel"], tag=plot_main_tag + "_x")
            dpg.add_plot_axis(dpg.mvYAxis, label=node_params["ylabel"], tag=plot_main_tag + "_y")
            dpg.add_heat_series(plot_data["data"], rows=plot_data["rows"], cols=plot_data["cols"], 
                                tag=plot_main_tag + "heat", parent=plot_main_tag + "_y", bounds_min=node_params["bounds_min"], 
                                bounds_max=node_params["bounds_max"], format="", scale_min=plot_data["scale_min"],
                                scale_max=plot_data["scale_max"])
            dpg.bind_colormap(plot_main_tag, node_params["colormap"])
        
        dpg.fit_axis_data(plot_main_tag + "_x")
        dpg.fit_axis_data(plot_main_tag + "_y")


class PairGridPlot(BasePlot):

    def plot(self, node_params, plot_data):
        data = np.array(plot_data["data"])
        if data.ndim == 1:
            return
        n_features = min(data.shape[1], 5)
        if plot_data["labels"] is None:
            feature_labels = [f"Var {i+1}" for i in range(n_features)]
        else:
            feature_labels = plot_data["labels"]
        
        labels_count = len(feature_labels)
        unique_labels = None
        if plot_data["target_label"] is not None and \
            plot_data["target_label"].shape[0] == data.shape[0]:
            unique_labels = np.unique(plot_data["target_label"])
            labels_count = len(unique_labels)
        
        self.clear_plot_region(node_params["region"])
        with dpg.subplots(label=f"{node_params['title']}",
                        rows=n_features, 
                          columns=n_features, 
                          parent=node_params["region"], 
                          height=-1, width=-1):
            for i in range(n_features):
                for j in range(n_features):
                    cell_tag = f"pairgrid_{i}_{j}_{dpg.generate_uuid()}"
                    with dpg.plot(label=f"{feature_labels[i]} vs {feature_labels[j]}", height=150, width=150, tag=cell_tag):
                        dpg.add_plot_legend()
                        x_axis_tag = cell_tag + "_x"
                        y_axis_tag = cell_tag + "_y"
                        
                        
                        if i == j:
                            dpg.add_plot_axis(dpg.mvXAxis, label="", tag=x_axis_tag)
                            dpg.add_plot_axis(dpg.mvYAxis, label="freq.", tag=y_axis_tag)

                            this_plot_tag = cell_tag + f"hist_{feature_labels[i]}"
                            this_plot_theme = cell_tag + f"hist_theme_{feature_labels[i]}"
                            dpg.add_histogram_series(data[:, i].tolist(), label=feature_labels[i], parent=y_axis_tag, tag=this_plot_tag)
                            self.create_histogram_theme(this_plot_theme, self.colors[(labels_count + i) % 30])
                            dpg.bind_item_theme(this_plot_tag, this_plot_theme)
                            self.track_tags[node_params["region"]].append(this_plot_theme)
                            self.track_tags[node_params["region"]].append(this_plot_tag)
                        else:
                            if i > j:
                                dpg.add_plot_axis(dpg.mvXAxis, label=feature_labels[j], tag=x_axis_tag)
                                dpg.add_plot_axis(dpg.mvYAxis, label=feature_labels[i], tag=y_axis_tag)
                                if unique_labels is not None:
                                    for idx, label in enumerate(unique_labels):
                                        indices = [k for k, l in enumerate(plot_data["target_label"]) if l == label]
                                        x = data[indices, j].tolist()
                                        y = data[indices, i].tolist()
                                        this_plot_tag = cell_tag + f"scatter_{label}_{idx}"
                                        dpg.add_scatter_series(x, y, label=f"{label}", parent=y_axis_tag, tag=this_plot_tag)
                                        this_plot_theme = cell_tag + f"_theme_{label}_{idx}"
                                        self.create_scatter_theme(this_plot_theme, self.colors[idx%30])
                                        dpg.bind_item_theme(this_plot_tag, this_plot_theme)
                                        self.track_tags[node_params["region"]].append(this_plot_theme)
                                        self.track_tags[node_params["region"]].append(this_plot_tag)
                                else:
                                    x = data[:, j].tolist()
                                    y = data[:, i].tolist()
                                    this_plot_tag_1 = cell_tag + f"scatter_{feature_labels[i]}_{feature_labels[j]}"
                                    this_plot_theme_1 = cell_tag + f"scatter_theme_{feature_labels[i]}_{feature_labels[j]}"
                                    dpg.add_scatter_series(x, y, label=f"{feature_labels[j]} vs {feature_labels[i]}", 
                                                           parent=y_axis_tag, tag=this_plot_tag_1)
                                    self.create_scatter_theme(this_plot_theme_1, self.colors[(labels_count + i) % 30])
                                    dpg.bind_item_theme(this_plot_tag_1, this_plot_theme_1)
                                    self.track_tags[node_params["region"]].append(this_plot_theme_1)
                                    self.track_tags[node_params["region"]].append(this_plot_tag_1)
                            else:
                                dpg.add_plot_axis(dpg.mvXAxis, label="", tag=x_axis_tag)
                                dpg.add_plot_axis(dpg.mvYAxis, label="freq.", tag=y_axis_tag)
                                y1 = data[:, j].tolist()
                                y2 = data[:, i].tolist()
                                this_plot_tag_1 = cell_tag + f"hist_{feature_labels[i]}_{feature_labels[j]}_1"
                                this_plot_theme_1 = cell_tag + f"hist_theme_{feature_labels[i]}_{feature_labels[j]}_1"
                                this_plot_tag_2 = cell_tag + f"hist_{feature_labels[i]}_{feature_labels[j]}_2"
                                this_plot_theme_2 = cell_tag + f"hist_theme_{feature_labels[i]}_{feature_labels[j]}_2"

                                dpg.add_histogram_series(y1, label=f"{feature_labels[i]}", parent=y_axis_tag, tag=this_plot_tag_1)
                                dpg.add_histogram_series(y2, label=f"{feature_labels[j]}", parent=y_axis_tag, tag=this_plot_tag_2)
                                self.create_histogram_theme(this_plot_theme_1, self.colors[(labels_count + i) % 30])
                                self.create_histogram_theme(this_plot_theme_2, self.colors[(labels_count + j) % 30])
                                dpg.bind_item_theme(this_plot_tag_1, this_plot_theme_1)
                                dpg.bind_item_theme(this_plot_tag_2, this_plot_theme_2)
                                self.track_tags[node_params["region"]].append(this_plot_theme_1)
                                self.track_tags[node_params["region"]].append(this_plot_theme_2)
                            
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

    
