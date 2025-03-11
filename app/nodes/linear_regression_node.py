import numpy as np
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
        self.feature_port_id = self.add_input_port("featuredata", [PortType.DATASERIESFLOAT, PortType.MODELSERIESFLOAT], "X Data")
        self.target_data_port_id = self.add_input_port("targetdata", [PortType.DATASERIESFLOAT, PortType.MODELSERIESFLOAT], "Y Data")
        self.fit_port_id = self.add_output_port("fitdata", PortType.MODELSERIESFLOAT, "Fit Line")



    def compute(self):
        print(f"[{self.node_id}] Computing Simple Linear Regression...")
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

            slope, intercept = np.polyfit(x, target_data, self.params["degree"])
            self.params["slope"] = slope
            self.params["intercept"] = intercept

            fit = slope * x + intercept

            self.params["r2_score"] = r2_score(target_data, fit)

            output_data ={self.fit_port_id: [x.tolist(), fit.tolist()]}
            self.store_data_in_ports(output_data)

            print(f"[{self.node_id}] Computation successful. R²: {self.params['r2_score']:.4f}")
            return True

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
        self.feature_port_id = self.add_input_port("featuredata", [PortType.DATAFRAMEFLOAT, PortType.MODELDATAFRAMEFLOAT], "Feature Data")
        self.target_data_port_id = self.add_input_port("targetdata", [PortType.DATASERIESFLOAT, PortType.MODELSERIESFLOAT], "Target Data")
        self.xaxis_port_id = self.add_input_port("xaxisdata", [PortType.DATASERIESFLOAT, PortType.MODELSERIESFLOAT], "X-axis Data")
        self.fit_port_id = self.add_output_port("fitdata", PortType.MODELSERIESFLOAT, "Fit Line")


    def compute(self):
        print(f"[{self.node_id}] Computing Linear Regression...")
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
            reg_model = LinearRegression(positive=self.params["nng"])
            reg_model.fit(X_train, y_train)

            self.params["r2_score"] = r2_score(y_test, reg_model.predict(X_test))
            self.model_params["coefficients"] = reg_model.coef_
            self.model_params["intercept"] = reg_model.intercept_

            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)
            fitted_line = reg_model.predict(feature_data)
            
            output_data = {self.fit_port_id: [x_axis_data.tolist(), fitted_line.tolist()]}
            self.store_data_in_ports(output_data)

            print(f"[{self.node_id}] Computation successful. R²: {self.params['r2_score']:.4f}")
            return True

        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")