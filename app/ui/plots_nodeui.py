import dearpygui.dearpygui as dpg
from app.ui.base_node_ui import BaseNodeUI
from app.utils.constants import PLOT_1_TAG, PLOT_2_TAG, PLOT_3_TAG, PLOT_4_TAG, PLOT_5_TAG, PLOT_6_TAG


class XYScatterPlotNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()


    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("XY Scatter Plot Node")
            dpg.add_separator()
            dpg.add_input_text(label="Title", hint="Enter the plot title here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_title")
            dpg.add_input_text(label="Plot Legend", hint="Enter the plot label here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_legend")
            dpg.add_input_text(label="Fit Legend", hint="Enter the fit label here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_fit_legend")
            dpg.add_input_text(label="X Label", hint="Enter the x-axis label here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_xlabel")
            dpg.add_input_text(label="Y Label", hint="Enter the y-axis label here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_ylabel")
            dpg.add_color_edit(label="Marker Color", default_value=(255, 255, 255, 255), 
                               tag=f"{self.ACTION_TAG}_{self.node_id}_marker_color")
            dpg.add_combo(label="Marker Style", 
                          items=["Circle", "Square", "Diamond", "Cross", "Plus", "Asterisk", "Triangle"],
                          default_value="Circle", 
                          tag=f"{self.ACTION_TAG}_{self.node_id}_style")
            
            dpg.add_color_edit(label="Line Color", default_value=(255, 0, 255, 255), 
                               tag=f"{self.ACTION_TAG}_{self.node_id}_line_color")
            dpg.add_combo(label="Plot Area", 
                          items=["Plot 1", "Plot 2", "Plot 3", "Plot 4", "Plot 5", "Plot 6"], 
                          default_value="Plot 1", 
                          tag=f"{self.ACTION_TAG}_{self.node_id}_plot_area")
            
            dpg.add_button(label="Save Changes", callback=self.popup_callback)

    def popup_callback(self):
        self.node_instance.params["title"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_title").strip()
        self.node_instance.params["plot_label"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_legend").strip()
        self.node_instance.params["fit_label"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_fit_legend").strip()
        self.node_instance.params["xlabel"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_xlabel").strip()
        self.node_instance.params["ylabel"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_ylabel").strip()
        self.node_instance.params["marker_color"] = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_marker_color")
        self.node_instance.params["line_color"] = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_line_color")


        marker_style = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_style")
        if marker_style == "Circle":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Circle
        elif marker_style == "Square":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Square
        elif marker_style == "Diamond":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Diamond
        elif marker_style == "Cross":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Cross
        elif marker_style == "Plus":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Plus
        elif marker_style == "Asterisk":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Asterisk
        elif marker_style == "Triangle":
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Up
        
        rg = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area")
        if rg == "Plot 1":
            self.node_instance.params["region"] = PLOT_1_TAG
        elif rg == "Plot 2":
            self.node_instance.params["region"] = PLOT_2_TAG
        elif rg == "Plot 3":
            self.node_instance.params["region"] = PLOT_3_TAG
        elif rg == "Plot 4":
            self.node_instance.params["region"] = PLOT_4_TAG
        elif rg == "Plot 5":
            self.node_instance.params["region"] = PLOT_5_TAG
        elif rg == "Plot 6":
            self.node_instance.params["region"] = PLOT_6_TAG

        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")

    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_title",
                      self.node_instance.params["title"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_legend",
                      self.node_instance.params["plot_label"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_fit_legend",
                      self.node_instance.params["fit_label"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_xlabel",
                      self.node_instance.params["xlabel"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_ylabel",
                      self.node_instance.params["ylabel"])
        dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_marker_color",
                      self.node_instance.params["marker_color"])
        dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_line_color",
                      self.node_instance.params["line_color"])
        
        
        marker_style = self.node_instance.params["marker_style"]
        
        if marker_style == dpg.mvPlotMarker_Circle:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Circle")
        elif marker_style == dpg.mvPlotMarker_Square:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Square")
        elif marker_style == dpg.mvPlotMarker_Diamond:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Diamond")
        elif marker_style == dpg.mvPlotMarker_Cross:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Cross")
        elif marker_style == dpg.mvPlotMarker_Plus:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Plus")
        elif marker_style == dpg.mvPlotMarker_Asterisk:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Asterisk")
        elif marker_style == dpg.mvPlotMarker_Up:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Triangle")
        else:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_style", "Circle")
            self.node_instance.params["marker_style"] = dpg.mvPlotMarker_Circle

        region = self.node_instance.params["region"]
        if region == PLOT_1_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 1")
        elif region == PLOT_2_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 2")
        elif region == PLOT_3_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 3")
        elif region == PLOT_4_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 4")
        elif region == PLOT_5_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 5")
        elif region == PLOT_6_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 6")


class HeatMapPlotNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("HeatMap Plot Node")
            dpg.add_separator()
            dpg.add_input_text(label="Title", hint="Enter the plot title here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_title")
            dpg.add_input_text(label="X Label", hint="Enter the x-axis label here.",
                               tag=f"{self.INPUT_TAG}_{self.node_id}_xlabel")
            dpg.add_input_text(label="Y Label", hint="Enter the y-axis label here.",
                               tag=f"{self.INPUT_TAG}_{self.node_id}_ylabel")
            
            dpg.add_input_floatx(label="XY bounds", default_value=[0, 0, 1, 1], 
                                 tag=f"{self.INPUT_TAG}_{self.node_id}_bounds")

            colormaps = sorted([
                        "Viridis", "Plasma", "BrBG", "Cool", "Dark", "Greys", "Deep", "Default",
                        "Hot", "Jet", "Paired", "Pastel", "Pink", "Spectral", "Twilight", "RdBu"
                    ], key=str.lower)
            dpg.add_combo(items=colormaps, 
                          label="Colormap", default_value="Viridis",
                          tag=f"{self.ACTION_TAG}_{self.node_id}_colormap")
            
            dpg.add_combo(label="Plot Area", tag=f"{self.ACTION_TAG}_{self.node_id}_plot_area",
                          items=["Plot 1", "Plot 2", "Plot 3", "Plot 4", "Plot 5", "Plot 6"], 
                          default_value="Plot 1")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
        
    def popup_callback(self):
        self.node_instance.params["title"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_title").strip()
        self.node_instance.params["xlabel"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_xlabel").strip()
        self.node_instance.params["ylabel"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_ylabel").strip()
        bounds = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_bounds")
        self.node_instance.params["bounds_min"]= [bounds[0], bounds[1]]
        self.node_instance.params["bounds_max"]= [bounds[2], bounds[3]]
        
        colormap = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_colormap")
        if colormap == "Viridis":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Viridis
        elif colormap == "Plasma":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Plasma
        elif colormap == "BrBG":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_BrBG
        elif colormap == "Cool":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Cool
        elif colormap == "Dark":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Dark
        elif colormap == "Greys":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Greys
        elif colormap == "Deep":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Deep
        elif colormap == "Default":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Default
        elif colormap == "Hot":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Hot
        elif colormap == "Jet":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Jet
        elif colormap == "Paired":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Paired
        elif colormap == "Pastel":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Pastel
        elif colormap == "Pink":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Pink
        elif colormap == "Spectral":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Spectral
        elif colormap == "Twilight":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Twilight
        elif colormap == "RdBu":
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_RdBu
    
        rg = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area")
        if rg == "Plot 1":
            self.node_instance.params["region"] = PLOT_1_TAG
        elif rg == "Plot 2":
            self.node_instance.params["region"] = PLOT_2_TAG
        elif rg == "Plot 3":
            self.node_instance.params["region"] = PLOT_3_TAG
        elif rg == "Plot 4":
            self.node_instance.params["region"] = PLOT_4_TAG
        elif rg == "Plot 5":
            self.node_instance.params["region"] = PLOT_5_TAG
        elif rg == "Plot 6":
            self.node_instance.params["region"] = PLOT_6_TAG

        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")

    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_title",
                      self.node_instance.params["title"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_xlabel",
                      self.node_instance.params["xlabel"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_ylabel",
                      self.node_instance.params["ylabel"])
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_bounds",
                      self.node_instance.params["bounds_min"] + self.node_instance.params["bounds_max"])
        
        colormap = self.node_instance.params["colormap"]
        
        if colormap == dpg.mvPlotColormap_Viridis:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Viridis")
        elif colormap == dpg.mvPlotColormap_Plasma:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Plasma")
        elif colormap == dpg.mvPlotColormap_BrBG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "BrBG")
        elif colormap == dpg.mvPlotColormap_Cool:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Cool")
        elif colormap == dpg.mvPlotColormap_Dark:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Dark")
        elif colormap == dpg.mvPlotColormap_Greys:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Greys")
        elif colormap == dpg.mvPlotColormap_Deep:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Deep")
        elif colormap == dpg.mvPlotColormap_Default:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Default")
        elif colormap == dpg.mvPlotColormap_Hot:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Hot")
        elif colormap == dpg.mvPlotColormap_Jet:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Jet")
        elif colormap == dpg.mvPlotColormap_Paired:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Paired")
        elif colormap == dpg.mvPlotColormap_Pastel:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Pastel")
        elif colormap == dpg.mvPlotColormap_Pink:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Pink")
        elif colormap == dpg.mvPlotColormap_Spectral:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Spectral")
        elif colormap == dpg.mvPlotColormap_Twilight:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Twilight")
        elif colormap == dpg.mvPlotColormap_RdBu:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "RdBu")
        else:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_colormap", "Viridis")
            self.node_instance.params["colormap"] = dpg.mvPlotColormap_Viridis
        region = self.node_instance.params["region"]
        if region == PLOT_1_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 1")
        elif region == PLOT_2_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 2")
        elif region == PLOT_3_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 3")
        elif region == PLOT_4_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 4")
        elif region == PLOT_5_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 5")
        elif region == PLOT_6_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 6")

class PairGridPlotNodeUI(BaseNodeUI):
    def __init__(self, node_instance):
        super().__init__(node_instance)
        self.INPUT_TAG = dpg.generate_uuid()
        self.ACTION_TAG = dpg.generate_uuid()
        self.POP_UP_TAG = dpg.generate_uuid()
    
    def node_popup(self):
        with dpg.popup(tag=f"{self.POP_UP_TAG}_{self.node_id}", 
                       parent=self.node_id):
            dpg.add_text("PairGrid Plot Node")
            dpg.add_separator()
            dpg.add_input_text(label="Title", hint="Enter the plot title here.", 
                               tag=f"{self.INPUT_TAG}_{self.node_id}_title")
            dpg.add_combo(label="Plot Area", tag=f"{self.ACTION_TAG}_{self.node_id}_plot_area",
                          items=["Plot 1", "Plot 2", "Plot 3", "Plot 4", "Plot 5", "Plot 6"], 
                          default_value="Plot 1")
            dpg.add_button(label="Save Changes", callback=self.popup_callback)
    
    def popup_callback(self):
        self.node_instance.params["title"] = dpg.get_value(f"{self.INPUT_TAG}_{self.node_id}_title").strip()
        
        rg = dpg.get_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area")
        if rg == "Plot 1":
            self.node_instance.params["region"] = PLOT_1_TAG
        elif rg == "Plot 2":
            self.node_instance.params["region"] = PLOT_2_TAG
        elif rg == "Plot 3":
            self.node_instance.params["region"] = PLOT_3_TAG
        elif rg == "Plot 4":
            self.node_instance.params["region"] = PLOT_4_TAG
        elif rg == "Plot 5":
            self.node_instance.params["region"] = PLOT_5_TAG
        elif rg == "Plot 6":
            self.node_instance.params["region"] = PLOT_6_TAG

        dpg.hide_item(f"{self.POP_UP_TAG}_{self.node_id}")
    
    def update_ui(self):
        dpg.set_value(f"{self.INPUT_TAG}_{self.node_id}_title",
                      self.node_instance.params["title"])
        
        region = self.node_instance.params["region"]
        if region == PLOT_1_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 1")
        elif region == PLOT_2_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 2")
        elif region == PLOT_3_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 3")
        elif region == PLOT_4_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 4")
        elif region == PLOT_5_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 5")
        elif region == PLOT_6_TAG:
            dpg.set_value(f"{self.ACTION_TAG}_{self.node_id}_plot_area", "Plot 6")
            