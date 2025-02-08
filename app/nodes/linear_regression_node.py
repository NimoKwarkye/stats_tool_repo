import pandas as pd
from app.core.node import Node

class LinearRegressionNode(Node):
    def __init__(self, node_id, name="Simple Linear Regression"):
        super().__init__(node_id, name)
        self.params = {"slope": 0,
                       "intercept": 0}  # filepath to CSV
        self.add_input_port("data", "DataFrame")
        self.add_output_port("fit", "Model")

    def compute(self):
        pass