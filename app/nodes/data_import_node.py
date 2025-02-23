import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app.core.node import Node



class CSVImportNode(Node):
    def __init__(self, node_id, name="CSV Import"):
        super().__init__(node_id, name)
        self.params = {"filepath": None,
                       "csv_sep": ","}  # filepath to CSV
        self.add_output_port("data", "DataFrame", "Data")
        self.add_output_port("labels", "Series", "Feature Labels")

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        
        filepath = self.params.get("filepath")
        if not filepath:
            raise ValueError("CSVImportNode: 'filepath' parameter is not set.")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSVImportNode: File not found at {filepath}")
        try:
            df = pd.read_csv(filepath, sep=self.params.get("csv_sep"))
        except Exception as e:
            raise RuntimeError(f"CSVImportNode: Error reading CSV file: {e}")
        # Store the result in the output port.
        for port in self.output_ports:
            if port.name.split("##")[0] == "data":
                port.value.append(df.to_numpy())
        return True



class SQLDBImportNode(Node):
    def __init__(self, node_id, name="SQL DB Import"):
        super().__init__(node_id, name)
        self.params = {"connection_string": None,
                       "data_query": None,
                       "labels_query": None}
        self.add_output_port("data", "DataFrame", "Data")
        self.add_output_port("labels", "Series", "Feature Labels")

    def compute(self):
        print(f"[{self.node_id}] Computing...")
        
        connection_string = self.params.get("connection_string")
        data_query = self.params.get("data_query")
        labels_query = self.params.get("labels_query")
        if not connection_string:
            raise ValueError("SQLImportNode: 'connection_string' parameter is not set.")
        if not data_query:
            raise ValueError("SQLImportNode: 'query' parameter is not set.")
        
        try:
            engine = create_engine(connection_string)
            with engine.connect() as connection:
                df = pd.read_sql(data_query, connection, dtype=np.float64)
                if labels_query:
                    labels = pd.read_sql(labels_query, connection, dtype=np.float64)
                    labels = labels[labels.columns[0]]
        except Exception as e:
            raise RuntimeError(f"SQLImportNode: Error reading SQL query: {e}")
        
        # Store the result in the output port.
        for port in self.output_ports:
            if port.name.split("##")[0] == "data":
                port.value.append(df.to_numpy())
            elif port.name.split("##")[0] == "labels" and labels_query:
                port.value.append(labels.to_numpy())
        return True