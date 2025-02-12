import numpy as np
from app.core.node import Node

class LinearRegressionNode(Node):
    def __init__(self, node_id, name="Simple Linear Regression"):
        super().__init__(node_id, name)
        self.params = {"slope": 0,
                       "intercept": 0}  # filepath to CSV
        self.add_input_port("data", "DataFrame")
        self.add_output_port("fit", "Model")

    def fit(self, data):
        prd = self.params["slope"] * data[:, 0] + self.params["intercept"]
        return prd

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        port_data = None
        for port in self.input_ports:
            if port.name.split("##")[0] == "data" and len(port.value) > 0:
                #get data from the input port
                port_data = port.value[0]
        #use the data to compute the slope and intercept
        if port_data is None:
            return False
        self.params["slope"], self.params["intercept"] = np.polyfit(port_data[:, 0], port_data[:, 1], 1)
        for port in self.output_ports:
            if port.name.split("##")[0] == "fit":
                port.value.clear()
                port.value.append(list(port_data[:, 0]))
                port.value.append(list(self.fit(port_data)))
            
        return True