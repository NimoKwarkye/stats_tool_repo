import numpy as np
from app.core.node import Node
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class SimpleLinearRegressionNode(Node):
    def __init__(self, node_id, name="Simple Linear Regression"):
        super().__init__(node_id, name)
        self.params = {
            "slope": 0,
            "intercept": 0,
            "degree": 1,      # Currently fixed to 1 (simple linear regression)
            "r2_score": 0,
        }
        self.add_input_port("featuredata", "DataFrame", "Feature Data")
        self.add_input_port("targetdata", "Series", "Target Data")
        self.add_output_port("fitdata", "Model", "Fit Line")

    def get_input_data(self):
        feature_data = None
        target_data = None
        for port in self.input_ports:
            key = port.name.split("##")[0]
            if key == "featuredata" and port.value:
                feature_data = port.value[0]
            elif key == "targetdata" and port.value:
                target_data = port.value[0]
        return feature_data, target_data

    def compute(self):
        print(f"[{self.node_id}] Computing Simple Linear Regression...")
        feature_data, target_data = self.get_input_data()
        if feature_data is None or target_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            # Convert inputs to NumPy arrays.
            feature_data = np.array(feature_data)
            target_data = np.array(target_data)

            # Ensure feature_data is 2D; use the first column for fitting.
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)
            x = feature_data[:, 0]

            # Compute slope and intercept using polyfit (degree 1).
            slope, intercept = np.polyfit(x, target_data, self.params["degree"])
            self.params["slope"] = slope
            self.params["intercept"] = intercept

            # Compute fitted values.
            fit = slope * x + intercept

            # Calculate R² score.
            self.params["r2_score"] = r2_score(target_data, fit)

            # Store results in the output port.
            for port in self.output_ports:
                if port.name.split("##")[0] == "fitdata":
                    port.value.clear()
                    port.value.append(x.tolist())
                    port.value.append(fit.tolist())

            print(f"[{self.node_id}] Computation successful. R²: {self.params['r2_score']:.4f}")
            return True

        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")

class LinearRegressionNode(Node):
    def __init__(self, node_id, name="Linear Regression"):
        super().__init__(node_id, name)
        self.params = {
            "test_size": 0.2,
            "nng": False,
            "r2_score": None,
            
        }
        self.model_params = {
            "coefficients": None,
            "intercept": None,
        }
        self.add_input_port("featuredata", "DataFrame", "Feature Data")
        self.add_input_port("targetdata", "Series", "Target Data")
        self.add_input_port("xaxisdata", "Series", "X-axis Data")
        self.add_output_port("fitdata", "Model", "Fit Line")

    def get_input_data(self):
        feature_data = None
        target_data = None
        for port in self.input_ports:
            key = port.name.split("##")[0]
            if key == "featuredata" and port.value:
                feature_data = port.value[0]
            elif key == "targetdata" and port.value:
                target_data = port.value[0]
            elif key == "xaxisdata" and port.value:
                x_axis_data = port.value[0]
        return feature_data, target_data, x_axis_data

    def compute(self):
        print(f"[{self.node_id}] Computing Linear Regression...")
        feature_data, target_data, x_axis_data = self.get_input_data()
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

            for port in self.output_ports:
                if port.name.split("##")[0] == "fitdata":
                    port.value.clear()
                    port.value.append(x_axis_data.tolist())
                    port.value.append(fitted_line.tolist())

            print(f"[{self.node_id}] Computation successful. R²: {self.params['r2_score']:.4f}")
            return True

        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")