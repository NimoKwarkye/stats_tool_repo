from app.core.node import Node



class XYScatterPlotNode(Node):
    def __init__(self, node_id, name="XY Scatter Plot"):
        super().__init__(node_id, name)
        self.params = {"x": None, "y": None, "trend line":None, "title": None}
        self.add_input_port("data", "DataFrame")
        self.add_input_port("fit", "Model")

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        port_data = None
        port_fit = None
        for port in self.input_ports:
            if port.name == "data" and len(port.value) > 0:
                port_data = port.value[0]
            elif port.name == "fit" and len(port.value) > 0:
                port_fit = port.value[0]
        if port_data is None:
            return False
        #set the x and y values from port_data
        #if port_fit is not None, set the trend line
        print(f"plotted {port_data} with {port_fit}")

        return True