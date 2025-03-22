import numpy as np
import pandas as pd
from app.core.node import Node
from app.core.port import PortType
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class LogisticRegressionNode(Node):
    def __init__(self, node_index, name="Logistic Regression"):
        super().__init__(node_index, name)
        self.params = {
            "penalty": "l2",
            "test_size": 0.3,
            "dual": False,
            "tol": 1e-4,
            "C": 1.0,
            "fit_intercept": True,
            "intercept_scaling": 1,
            "class_weight": None,
            "random_state": None,
            "solver": "lbfgs",
            "max_iter": 100,
            "warm_start": False,
            "n_jobs": None,
            "l1_ratio": None,
            "score": 0,
        }
        self.lgr = None
        self.feature_port_id = self.add_input_port("featuredata", 
                                                   [PortType.DATAFRAMEFLOAT, 
                                                    PortType.MODELDATAFRAMEFLOAT], 
                                                    "Feature Data", True)
        self.feature_labels_port_id = self.add_input_port("featurelabels", 
                                                          PortType.FEATURELABELSSTRING, 
                                                          "Feature Labels")
        self.target_port_id = self.add_input_port("targetdata", 
                                                  [PortType.DATASERIESFLOAT, 
                                                   PortType.MODELSERIESFLOAT], 
                                                   "Target Data", True)
        self.sample_weight_port_id = self.add_input_port("sampleweightdata", 
                                                  [PortType.DATASERIESFLOAT, 
                                                   PortType.MODELSERIESFLOAT], 
                                                   "Sample Weights")

        self.class_data_port_id = self.add_output_port("logisticregressionfitdata", 
                                                     PortType.TARGETLABELSSTRING, 
                                                     "Logistic Regression Classes")
        self.coef_port_id = self.add_output_port("logisticregressioncoefdata", 
                                                 PortType.MODELDATAFRAMEFLOAT, 
                                                 "Logistic Regression Coefficients")
        
        self.model_port_id = self.add_output_port("logisticregressionmodel",
                                                  PortType.MODELOBJECT, 
                                                  "Logistic Regression Model")


    def pre_save(self):
        input_data = self.get_input_data()
        data = self.get_output_data()
        feature_labels = input_data.get(self.feature_labels_port_id)
        save_dir = self.compose_dir_name(self.feature_port_id)
        coefs = data.get(self.coef_port_id)
        classes = data.get(self.class_data_port_id)

        labels = None
        if feature_labels is not None:
            labels = [f"{i}_coef" for i in feature_labels]
        else:
            feature_count = coefs.shape[1] - 1
            labels = [f"coef_{i+1}" for i in range(feature_count)]
        data_to_save = { }
        coef_dict = {"intercept": coefs[:, 0]}
        for i, label in enumerate(labels):
            coef_dict[label] = coefs[:, i+1]
        data_to_save["logistic_regression_coefficients"] = pd.DataFrame(coef_dict)
        data_to_save["logistic_regression_classes"] = pd.DataFrame({"classes": classes})

        return save_dir, data_to_save, {"logistic_regression_model": self.lgr}

  

    def compute(self):
        ret_data = self.get_input_data()
        feature_data = ret_data.get(self.feature_port_id)
        target_data = ret_data.get(self.target_port_id)
        sample_weight_data = ret_data.get(self.sample_weight_port_id)
        if feature_data is None or target_data is None:
            raise ValueError("Missing required data")
        
        try:
            self.lgr = LogisticRegression(
                penalty=self.params["penalty"],
                dual=self.params["dual"],
                tol=self.params["tol"],
                C=self.params["C"],
                fit_intercept=self.params["fit_intercept"],
                intercept_scaling=self.params["intercept_scaling"],
                class_weight=self.params["class_weight"],
                random_state=self.params["random_state"],
                solver=self.params["solver"],
                max_iter=self.params["max_iter"],
                warm_start=self.params["warm_start"],
                n_jobs=self.params["n_jobs"],
                l1_ratio=self.params["l1_ratio"],
            )
            X_train, X_test, y_train, y_test, weight_train, weight_test = None, None, None, None, None, None
            if sample_weight_data is None:
                X_train, X_test, y_train, y_test = train_test_split(
                    feature_data, target_data, test_size=self.params["test_size"],
                    random_state=42
                    )
            else:
                X_train, X_test, y_train, y_test, weight_train, weight_test = train_test_split(
                feature_data, target_data, sample_weight_data, test_size=self.params["test_size"])
            


            self.lgr = self.lgr.fit(X_train, y_train, weight_train)
            classes = self.lgr.predict(feature_data)
            train_score = self.lgr.score(X_train, y_train, weight_train)
            test_score = self.lgr.score(X_test, y_test, weight_test)
            unique_classes = np.unique(classes)
            return_log = f"Train Score: {train_score}\nTest Score: {test_score}\nclasses: {unique_classes.tolist()}\niterations: {self.lgr.n_iter_}"
            self.params["score"] = self.lgr.score(feature_data, target_data, sample_weight_data)

            intercept = self.lgr.intercept_
            if intercept.ndim == 1:
                intercept = intercept.reshape(-1, 1)
            coef = self.lgr.coef_
            if coef.ndim == 1:
                coef = coef.reshape(-1, 1)
            coef = np.concat((intercept, coef), axis=1)

            output_data = {
                self.class_data_port_id: classes,
                self.coef_port_id: coef,
                self.model_port_id: self.lgr,
            }
            self.store_data_in_ports(output_data)
            return return_log
        
        except Exception as e:
            raise RuntimeError(f"[{self.node_id}] Error during computation: {e}")
        