import numpy as np
from app.core.node import Node
from app.core.port import PortType

class XYScatterPlotNode(Node):
    def __init__(self, node_index, name="XY Scatter Plot"):
        super().__init__(node_index, name)
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
            "plot_type":"scatter"
        }
        self.plot_data = {
            "x": None, 
            "y": None, 
            "trend_line": [],
        }
        self.xaxisdata_port_id = self.add_input_port("xaxisdata", PortType.DATASERIESFLOAT, "X Data")
        self.targetdata_port_id = self.add_input_port("targetdata", PortType.DATASERIESFLOAT, "Y Data")
        self.fitdata_port_id = self.add_input_port("fitdata", PortType.MODELSERIESFLOAT, "Fit Line")
    
    def get_port_value(self):
        """Helper that returns the first value of the input port with the given key."""
        ret_data = {}
        for port in self.input_ports:
            if port.connection in port.value:
                ret_data[port.port_id] = port.value[port.connection]
        x_data = ret_data.get(self.xaxisdata_port_id)
        y_data = ret_data.get(self.targetdata_port_id)
        fit_data = ret_data.get(self.fitdata_port_id)
        return x_data, y_data, fit_data

    def compute(self):
        print(f"[{self.node_id}] Computing XY Scatter Plot...")
        x_data, y_data, port_fit = self.get_port_value()
        
        if x_data is None or y_data is None:
            raise ValueError(f"[{self.node_id}] Missing required X or Y data.")
        
        self.plot_data["x"] = list(x_data)
        self.plot_data["y"] = list(y_data)
        
        if port_fit is not None and len(port_fit) >= 2:
            # Store both x-values and trend line.
            self.plot_data["trend_line"] = [port_fit[0], port_fit[1]]
        else:
            self.plot_data["trend_line"] = []
        
        self.has_data = True
        return True


class HeatMapPlotNode(Node):
    def __init__(self, node_index, name="HeatMap Plot"):
        super().__init__(node_index, name)
        self.has_data = False
        self.params = {
            "title": "title", 
            "xlabel": "x", 
            "ylabel": "y",
            "region": "plot_1",
            "colormap": 0,
            "bounds_min": [0, 0],
            "bounds_max": [1, 1],
            "plot_type": "heatmap",
        }
        self.plot_data = {
            "data": None, 
            "scale_max": None,
            "rows": None,
            "cols": None, 
            "scale_min": None,
        }
        self.feature_port_id = self.add_input_port("featuredata", PortType.DATAFRAMEFLOAT, "Feature Data")
    
    def get_port_value(self):
        """Helper that returns the first value of the input port with the given key."""
        for port in self.input_ports:

            if port.connection in port.value:
                return port.value[port.connection]
        return None

    def compute(self):
        print(f"[{self.node_id}] Computing HeatMap Plot...")
        port_data = self.get_port_value()
        if port_data is None:
            raise ValueError("HeatMapPlot: No data provided")
        
        # Expecting port_data to be a NumPy array or convertible
        port_data = np.array(port_data)
        self.plot_data["rows"] = port_data.shape[0]
        self.plot_data["cols"] = port_data.shape[1]
        self.plot_data["scale_max"] = port_data.max()
        self.plot_data["scale_min"] = port_data.min()
        # Flatten data for storage or plotting library compatibility.
        self.plot_data["data"] = port_data.flatten().tolist()
        self.has_data = True
        return True


class PairGridPlotNode(Node):
    def __init__(self, node_index, name="PairGrid Plot"):
        super().__init__(node_index, name)
        self.has_data = False
        self.params = {
            "title": "title", 
            "region": "plot_1",
            "plot_type": "pairgrid",
        }
        self.plot_data = {
            "data": None, 
            "labels": None,
        }
        self.feature_port_id = self.add_input_port("featuredata", PortType.DATAFRAMEFLOAT, "Feature Data")
        self.labels_port_id = self.add_input_port("featurelabels", PortType.DATASERIESSTRING, "Feature Labels")
    
    def get_port_value(self):
        """Helper that returns the first value of the input port with the given key."""
        ret_data = {}
        for port in self.input_ports:
            if port.connection in port.value:
                ret_data[port.port_id] = port.value[port.connection]
        feature_data = ret_data.get(self.feature_port_id)
        feature_labels = ret_data.get(self.labels_port_id)
        return feature_data, feature_labels

    def compute(self):
        print(f"[{self.node_id}] Computing PairGrid Plot...")
        feature_data, feature_labels = self.get_port_value()
        if feature_data is None:
            raise ValueError("PairGridPlot: No data provided")
        
        self.plot_data["data"] = feature_data
        self.plot_data["labels"] = feature_labels
        self.has_data = True
        return True