import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app.core.node import Node

class CSVImportNode(Node):
    def __init__(self, node_id, name="CSV Import"):
        super().__init__(node_id, name)
        self.params = {
            "filepath": None,
            "csv_sep": ",",
            "target_col": None,
            "xaxis_col": None,
            "drop_cols": None,
            "header": True,
            "drop_xaxis": False,
        }
        self.add_output_port("featuredata", "DataFrame", "Feature Data")
        self.add_output_port("xaxisdata", "Series", "X-axis Data")
        self.add_output_port("targetdata", "Series", "Target Data")
        self.add_output_port("featurelabels", "Series", "Feature Labels")
    
    def load_csv_data(self):
        filepath = self.params.get("filepath")
        if not filepath:
            raise ValueError("CSVImportNode: 'filepath' parameter is not set.")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSVImportNode: File not found at {filepath}")
        try:
            headers = "infer" if self.params.get("header") else None
            df = pd.read_csv(filepath, sep=self.params.get("csv_sep"), header=headers)
            if len(self.params.get("drop_cols")) > 0:
                df = df.drop(self.params.get("drop_cols"), axis=1)
            target = None
            if self.params.get("target_col"):
                target = df[self.params.get("target_col")]
                df = df.drop(self.params.get("target_col"), axis=1)
            xaxis = None
            if self.params.get("xaxis_col"):
                xaxis = df[self.params.get("xaxis_col")]
                if self.params.get("drop_xaxis"):
                    df = df.drop(self.params.get("xaxis_col"), axis=1)
        except Exception as e:
            raise RuntimeError(f"CSVImportNode: Error reading CSV file: {e}")
        # Return a dictionary containing the imported data.
        return {
            "xaxisdata": xaxis.to_numpy() if xaxis is not None else None,
            "featurelabels": df.columns.values,
            "featuredata": df.to_numpy(),
            "targetdata": target.to_numpy() if target is not None else None,
            # Additional data (e.g. labels) can be added here as needed.
        }
    
    def store_data_in_ports(self, data):
        for port in self.output_ports:
            key = port.name.split("##")[0]
            if key in data and data[key] is not None:
                port.value.clear()
                port.value.append(data[key])
    
    def compute(self):
        print(f"[{self.node_id}] Computing CSV Import...")
        data = self.load_csv_data()
        self.store_data_in_ports(data)
        return True


class SQLDBImportNode(Node):
    def __init__(self, node_id, name="SQL DB Import"):
        super().__init__(node_id, name)
        self.params = {
            "connection_string": None,
            "data_query": None,
            "target_query": None,
            "xaxis_query": None,
        }
        self.add_output_port("featuredata", "DataFrame", "Feature Data")
        self.add_output_port("xaxisdata", "Series", "X-axis Data")
        self.add_output_port("targetdata", "Series", "Target Data")
        self.add_output_port("featurelabels", "Series", "Feature Labels")
    
    def load_sql_data(self):
        connection_string = self.params.get("connection_string")
        data_query = self.params.get("data_query")
        target_query = self.params.get("target_query")
        xaxis_query = self.params.get("xaxis_query")
        if not connection_string:
            raise ValueError("SQLImportNode: 'connection_string' parameter is not set.")
        if not data_query:
            raise ValueError("SQLImportNode: 'data_query' parameter is not set.")
        try:
            engine = create_engine(connection_string)
            with engine.connect() as connection:
                df = pd.read_sql(data_query, connection, dtype=np.float64)
                target = None
                if target_query:
                    target = pd.read_sql(target_query, connection, dtype=np.float64)
                    target = target[target.columns[0]]
                if xaxis_query:
                    xaxis = pd.read_sql(xaxis_query, connection, dtype=np.float64)
                    xaxis = xaxis[xaxis.columns[0]]
        except Exception as e:
            raise RuntimeError(f"SQLImportNode: Error reading SQL query: {e}")
        return {
            "xaxisdata": xaxis.to_numpy() if xaxis is not None else None,
            "featurelabels": df.columns.values,
            "featuredata": df.to_numpy(),
            "targetdata": target.to_numpy() if target is not None else None,
            # If target data comes from SQL you can add it here.
        }
    
    def store_data_in_ports(self, data):
        for port in self.output_ports:
            key = port.name.split("##")[0]
            if key in data and data[key] is not None:
                port.value.clear()
                port.value.append(data[key])
    
    def compute(self):
        print(f"[{self.node_id}] Computing SQL DB Import...")
        data = self.load_sql_data()
        self.store_data_in_ports(data)
        return True