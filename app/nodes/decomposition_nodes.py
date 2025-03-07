import numpy as np
from app.core.node import Node
from sklearn.decomposition import PCA
from app.core.port import PortType

class PCANode(Node):
    def __init__(self, node_index, name="PCA"):
        super().__init__(node_index, name)
        self.params = {
            "n_components": 1,
            "copy_data": True,
            "whiten": False,
            "svd_solver": "auto",
            "tol": 0.0,
            "iterated_power": "auto",
            "random_state": None,
            "power_iteration_normalizer": "auto",
            "n_over_samples": 10,
        }
        self.feature_port_id = self.add_input_port("featuredata", PortType.DATAFRAMEFLOAT, "Feature Data")
        self.labels_port_id = self.add_input_port("featurelabels", PortType.DATASERIESSTRING, "Feature Labels")
        self.fit_data_port_id = self.add_output_port("fitdata_components", PortType.DATAFRAMEFLOAT, "PCA Components")
        self.loadings_port_id = self.add_output_port("fitdata_loadings", PortType.MODELDATAFRAMEFLOAT, "PCA Loadings")
        self.explained_variance_port_id = self.add_output_port("fitdata_expl", PortType.MODELSERIESFLOAT, 
                                                               "Explained Variance")
    
    def get_input_data(self):
        ret_data = {}
        for port in self.input_ports:
            key = port.connection
            if key in port.value:
                ret_data[port.port_id] = port.value[key]
        feature_data = ret_data.get(self.feature_port_id, None)
        feature_labels = ret_data.get(self.labels_port_id, None)

        return feature_data, feature_labels

    def compute(self):
        print(f"[{self.node_id}] Computing PCA...")
        feature_data, feature_labels = self.get_input_data()
        if feature_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
            if feature_labels is not None:
                feature_labels = np.array(feature_labels)
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)

            pca = PCA(
                n_components=self.params["n_components"],
                copy=self.params["copy_data"],
                whiten=self.params["whiten"],
                svd_solver=self.params["svd_solver"],
                tol=self.params["tol"],
                iterated_power=self.params["iterated_power"],
                random_state=self.params["random_state"],
                power_iteration_normalizer=self.params["power_iteration_normalizer"],
                n_over_samples=self.params["n_over_samples"],
            )
            pca.fit(feature_data)
            pca_components = pca.transform(feature_data)
            pca_loadings = pca.components_
            pca_explained_variance = pca.explained_variance_ratio_

            for port in self.output_ports:
                if port.port_id == self.fit_data_port_id:
                    port.value[self.fit_data_port_id] = pca_components
                elif port.port_id == self.loadings_port_id:
                    port.value[self.loadings_port_id] = pca_loadings
                elif port.port_id == self.explained_variance_port_id:
                    port.value[self.explained_variance_port_id] = pca_explained_variance


        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing PCA: {e}")