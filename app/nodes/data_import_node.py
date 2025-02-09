import os
import pandas as pd
from app.core.node import Node



class CSVImportNode(Node):
    def __init__(self, node_id, name="CSV Import"):
        super().__init__(node_id, name)
        self.params = {"filepath": None,
                       "csv_sep": ","}  # filepath to CSV
        self.add_output_port("data", "DataFrame")
        self.add_output_port("labels", "Series")

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        for port in self.output_ports:
            if port.name == "data":
                port.value.clear()
                port.value.append(f"{self.node_id}_df") 
        '''filepath = self.params.get("filepath")
        if not filepath:
            raise ValueError("CSVImportNode: 'filepath' parameter is not set.")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSVImportNode: File not found at {filepath}")
        try:
            df = pd.read_csv(filepath, sep=self.params.get("csv_sep"))
        except Exception as e:
            #TODO performing logging to the user
            pass
        # Store the result in the output port.
        for port in self.output_ports:
            if port.name == "data":
                port.value = df
        print(f"[{self.node_id}] Imported data from {filepath}")'''
        return True