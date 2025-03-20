
import os

import unittest
import os
import tempfile
import pandas as pd

from app.nodes.data_import_node import CSVImportNode

class TestCSVImportNode(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "test.csv")
        
        self.df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [5, 6, 7, 8],
            "target": [0, 1, 0, 1]
        })
        self.df.to_csv(self.csv_path, index=False)
        
        self.node = CSVImportNode(node_index=0)
        
        # Set node parameters.
        self.node.params["filepath"] = self.csv_path
        self.node.params["csv_sep"] = ","
        self.node.params["target_col"] = "target"
        self.node.params["xaxis_col"] = ""
        self.node.params["drop_cols"] = []  # No additional columns to drop.
        self.node.params["target_label_col"] = ""
        self.node.params["header"] = True
        self.node.params["drop_xaxis"] = False

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_csv_data(self):
        return_log = self.node.compute()
        data = self.node.get_output_data()
        
        # Check that expected keys are in the returned dictionary.
        self.assertIn(self.node.feature_port_id, data)
        self.assertIn(self.node.labels_port_id, data)
        self.assertIn(self.node.target_data_port_id, data)
        
        feature_data = data[self.node.feature_port_id]
        self.assertEqual(feature_data.shape, (4, 2))
        
        target_data = data[self.node.target_data_port_id]
        self.assertEqual(len(target_data), 4)
        
        self.assertIsInstance(return_log, str)

