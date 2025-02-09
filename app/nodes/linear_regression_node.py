import numpy as np
from app.core.node import Node

class LinearRegressionNode(Node):
    def __init__(self, node_id, name="Simple Linear Regression"):
        super().__init__(node_id, name)
        self.params = {"slope": 0,
                       "intercept": 0}  # filepath to CSV
        self.add_input_port("data", "DataFrame")
        self.add_output_port("fit", "Model")

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        port_data = None
        for port in self.input_ports:
            if port.name == "data" and len(port.value) > 0:
                #get data from the input port
                port_data = port.value
                print(port_data)
        #use the data to compute the slope and intercept
        for port in self.output_ports:
            if port.name == "fit":
                port.value.clear()
                port.value.append(f"{self.node_id}_fit")
            
        return True