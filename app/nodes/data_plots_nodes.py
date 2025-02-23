from app.core.node import Node



class XYScatterPlotNode(Node):
    def __init__(self, node_id, name="XY Scatter Plot"):
        super().__init__(node_id, name)
        self.has_data = False
        self.params = {
                     
                    "title": "title", 
                    "plot_label": "observation", 
                    "fit_label": "fit", 
                    "xlabel": "x", 
                    "ylabel": "y",
                    "marker_style": 0,
                    "region": "plot_1",
                    "marker_color": (255, 255, 55, 255),
                    "line_color": (255, 155, 55, 255),
                    }
        self.plot_data= {   "x": None, 
                            "y": None, 
                            "trend_line":[],
                            }
        self.add_input_port("data", "DataFrame")
        self.add_input_port("fit", "Model")


    

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        port_data = None
        port_fit = None
        for port in self.input_ports:
            if port.name.split("##")[0] == "data" and len(port.value) > 0:
                port_data = port.value[0]
            elif port.name.split("##")[0]=="fit" and len(port.value) > 0:
                port_fit = port.value
        
        if port_data is None:
            raise ValueError("XYScatterPlot: No data provided")
        #set the x and y values from port_data
        #if port_fit is not None, set the trend line
        self.plot_data["x"] = list(port_data[:, 0])
        self.plot_data["y"] = list(port_data[:, 1])
        if port_fit is not None:
            self.plot_data["trend_line"].append(port_fit[0])
            self.plot_data["trend_line"].append(port_fit[1])
        self.has_data = True
        return True


class HeatMapPlotNode(Node):

    def __init__(self, node_id, name="HeatMap Plot"):
        super().__init__(node_id, name)
        self.has_data = False
        self.params = {
                     
                    "title": "title", 
                    "xlabel": "x", 
                    "ylabel": "y",
                    "region": "plot_1",
                    "colormap": 0,
                    "bounds_min":[0, 0],
                    "bounds_max":[1, 1],
                    }
        self.plot_data= {   "data": None, 
                            "scale_max": None,
                            "rows": None,
                            "cols": None, 
                            "scale_min":None,
                            }
        self.add_input_port("data", "DataFrame")
    

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        port_data = None
        for port in self.input_ports:
            if port.name.split("##")[0] == "data" and len(port.value) > 0:
                port_data = port.value[0]
        
        if port_data is None:
            raise ValueError("HeatMapPlot: No data provided")
        
        self.plot_data["rows"] = port_data.shape[0]
        self.plot_data["cols"] = port_data.shape[1]
        self.plot_data["scale_max"] = port_data.max()
        self.plot_data["scale_min"] = port_data.min()
        self.plot_data["data"] = list(port_data.flatten())
        self.has_data = True
        return True