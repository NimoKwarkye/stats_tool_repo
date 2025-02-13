from app.core.node import Node



class XYScatterPlotNode(Node):
    def __init__(self, node_id, name="XY Scatter Plot"):
        super().__init__(node_id, name)
        self.has_data = False
        self.params = {
                     
                    "title": None, 
                    "xlabel": "x", 
                    "ylabel": "y",
                    "type": "scatter",
                    "region": None,
                    "marker_color": None,
                    "line_color": None,
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
            print("No data")
            return False
        #set the x and y values from port_data
        #if port_fit is not None, set the trend line
        self.plot_data["x"] = list(port_data[:, 0])
        self.plot_data["y"] = list(port_data[:, 1])
        if port_fit is not None:
            self.plot_data["trend_line"].append(port_fit[0])
            self.plot_data["trend_line"].append(port_fit[1])
        self.has_data = True
        return True