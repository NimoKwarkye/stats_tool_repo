import numpy as np
from app.core.node import Node
from sklearn.decomposition import PCA

class PCANode(Node):
    def __init__(self, node_id, name="PCA"):
        super().__init__(node_id, name)
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
        self.add_input_port("featuredata", "DataFrame", "Feature Data")
        self.add_input_port("featurelabels", "Series", "Feature Labels")
        self.add_output_port("fitdata", "DataFrame", "PCA Components")
        #self.add_output_port("fitdata", "Model", "PCA Loadings")
        #self.add_output_port("fitdata_expl", "Model", "Explained Variance")

    
    def get_input_data(self):
        feature_data = None
        feature_labels = None
        for port in self.input_ports:
            key = port.name.split("##")[0]
            if key == "featuredata" and port.value:
                feature_data = port.value[0]
            elif key == "featurelabels" and port.value:
                feature_labels = port.value[0]
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
                if port.name.split("##")[0] == "fitdata":
                    self.output_ports[0].value.append(pca_components)
                    #self.output_ports[1].value = pca_loadings
                    #self.output_ports[2].value = pca_explained_variance

        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing PCA: {e}")