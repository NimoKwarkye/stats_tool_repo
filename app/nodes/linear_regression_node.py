import numpy as np
import pandas as pd
from app.core.node import Node
from app.core.port import PortType
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class SimpleLinearRegressionNode(Node):
    def __init__(self, node_index, name="Simple Linear Regression"):
        super().__init__(node_index, name)
        self.params = {
            "slope": 0,
            "intercept": 0,
            "degree": 1,      # Currently fixed to 1 (simple linear regression)
            "r2_score": 0,
        }
        self.feature_port_id = self.add_input_port("featuredata", 
                                                   [PortType.DATASERIESFLOAT, 
                                                    PortType.MODELSERIESFLOAT], 
                                                    "X Data", True)
        self.target_data_port_id = self.add_input_port("targetdata", 
                                                       [PortType.DATASERIESFLOAT, 
                                                        PortType.MODELSERIESFLOAT], 
                                                        "Y Data", True)
        self.fit_port_id = self.add_output_port("fitdata", PortType.MODELSERIESFLOAT, "Fit Line")

    def pre_save(self):
        save_data = {
            
        }
        save_data["intercept"] = [self.params["intercept"]]
        for i in range(len(self.params["slope"])):
            save_data[f"coef_{i+1}"] = [self.params["slope"][i]]
        
        df = pd.DataFrame(save_data)
        return [self.compose_dir_name(self.feature_port_id), {"simple_linear_regression": df}, None]

    def compute(self):
        ret_data = self.get_input_data()
        feature_data = ret_data.get(self.feature_port_id)
        target_data = ret_data.get(self.target_data_port_id)

        if feature_data is None or target_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
            target_data = np.array(target_data)

            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)
            x = feature_data[:, 0]

            slope = np.polyfit(x, target_data, self.params["degree"])
            intercept = slope[-1]
            self.params["slope"] = slope
            self.params["intercept"] = intercept

            fit = slope * x + intercept

            self.params["r2_score"] = r2_score(target_data, fit)

            output_data ={self.fit_port_id: [x.tolist(), fit.tolist()]}
            self.store_data_in_ports(output_data)

            return_log = f"R² score: {self.params['r2_score']:.4f}\ncoefficients: {slope.tolist()}"
            return return_log

        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")

class LinearRegressionNode(Node):
    def __init__(self, node_index, name="Linear Regression"):
        super().__init__(node_index, name)
        self.params = {
            "test_size": 0.2,
            "nng": False,
            "r2_score": None,
            
        }
        self.model_params = {
            "coefficients": None,
            "intercept": None,
        }
        self.reg_model = None
        self.feature_port_id = self.add_input_port("featuredata", 
                                                   [PortType.DATAFRAMEFLOAT, 
                                                    PortType.MODELDATAFRAMEFLOAT], 
                                                    "Feature Data", True)
        self.feature_labels_port_id = self.add_input_port("featurelabels", [PortType.FEATURELABELSSTRING], "Feature Labels")
        self.target_data_port_id = self.add_input_port("targetdata", 
                                                       [PortType.DATASERIESFLOAT, 
                                                        PortType.MODELSERIESFLOAT], 
                                                        "Target Data", True)
        
        self.xaxis_port_id = self.add_input_port("xaxisdata", [PortType.DATASERIESFLOAT, PortType.MODELSERIESFLOAT], "X-axis Data")
        self.fit_port_id = self.add_output_port("fitdata", PortType.MODELSERIESFLOAT, "Fit Line")

    def pre_save(self):
        input_data = self.get_input_data()
        feature_labels = input_data.get(self.feature_labels_port_id)
        save_dir = self.compose_dir_name(self.feature_port_id)

        labels = None
        if feature_labels is not None:
            labels = [f"{i}_coef" for i in feature_labels]
        else:
            feature_count = self.model_params["coefficients"].shape[1]
            labels = [f"coef_{i+1}" for i in range(feature_count)]
        data_to_save = { }
        target_count = self.model_params["coefficients"].shape[0]
        for i in range(target_count):
            if i == 0:
                data_to_save["intercept"] = [self.model_params["intercept"][i]]
            else:
                data_to_save[f"target_{i}"].append(self.model_params["intercept"][i])
            
            for j in range(feature_count):
                if i == 0:
                    data_to_save[labels[j]] = [self.model_params["coefficients"][i, j]]
                else:
                    data_to_save[labels[j]].append(self.model_params["coefficients"][i, j])

        df = pd.DataFrame(data_to_save)
        return [save_dir, {"linear_regression": df}, {"linear_regression_model": self.reg_model}]


    def compute(self):
        ret_data = self.get_input_data()
        feature_data = ret_data.get(self.feature_port_id)
        target_data = ret_data.get(self.target_data_port_id)
        x_axis_data = ret_data.get(self.xaxis_port_id)

        if feature_data is None or target_data is None or x_axis_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
            target_data = np.array(target_data)
            x_axis_data = np.array(x_axis_data)
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)

            X_train, X_test, y_train, y_test = train_test_split(
                feature_data, target_data, test_size=self.params["test_size"]
            )
            self.reg_model = LinearRegression(positive=self.params["nng"])
            self.reg_model.fit(X_train, y_train)
            train_score = self.reg_model.score(X_train, y_train)
            test_score = self.reg_model.score(X_test, y_test)
            return_log = f"Train score: {train_score:.4f}\nTest score: {test_score:.4f}\nX rank: {self.reg_model.rank_}\nfeatures seen: {self.reg_model.n_features_in_}"

            self.params["r2_score"] = r2_score(y_test, self.reg_model.predict(X_test))
            self.model_params["coefficients"] = self.reg_model.coef_
            self.model_params["intercept"] = self.reg_model.intercept_

            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)
            fitted_line = self.reg_model.predict(feature_data)
            
            output_data = {self.fit_port_id: [x_axis_data.tolist(), fitted_line.tolist()]}
            self.store_data_in_ports(output_data)

            return return_log

        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")