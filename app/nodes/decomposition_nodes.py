import numpy as np
from app.core.node import Node
from sklearn.decomposition import PCA, NMF
from app.core.port import PortType

class PCANode(Node):
    def __init__(self, node_index, name="Principal Component Analysis"):
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
        self.feature_port_id = self.add_input_port("featuredata", [PortType.DATAFRAMEFLOAT, PortType.MODELDATAFRAMEFLOAT], "Feature Data")
        self.fit_data_port_id = self.add_output_port("fitdata_components", PortType.MODELDATAFRAMEFLOAT, "PCA Components")
        self.loadings_port_id = self.add_output_port("fitdata_loadings", PortType.MODELDATAFRAMEFLOAT, "PCA Loadings")
        self.explained_variance_port_id = self.add_output_port("fitdata_expl", PortType.MODELSERIESFLOAT, 
                                                               "Explained Variance")
        self.pca_component_names = self.add_output_port("pca_component_names", PortType.DATASERIESSTRING,
                                                        "PCA Component Labels")
    
    def get_input_data(self):
        ret_data = {}
        for port in self.input_ports:
            key = port.connection
            if key in port.value:
                ret_data[port.port_id] = port.value[key]
        feature_data = ret_data.get(self.feature_port_id, None)

        return feature_data

    def compute(self):
        print(f"[{self.node_id}] Computing PCA...")
        feature_data = self.get_input_data()
        if feature_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
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
                n_oversamples=self.params["n_over_samples"],
            )
            pca.fit(feature_data)
            pca_components = pca.transform(feature_data)
            pca_loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
            pca_explained_variance = pca.explained_variance_ratio_
            pca_component_names = [f"PC{i+1}" for i in range(pca.n_components_)]

            for port in self.output_ports:
                if port.port_id == self.fit_data_port_id:
                    port.value[self.fit_data_port_id] = pca_components
                elif port.port_id == self.loadings_port_id:
                    port.value[self.loadings_port_id] = pca_loadings
                elif port.port_id == self.explained_variance_port_id:
                    port.value[self.explained_variance_port_id] = pca_explained_variance
                elif port.port_id == self.pca_component_names:
                    port.value[self.pca_component_names] = pca_component_names


        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing PCA: {e}")


class NMFNode(Node):
    def __init__(self, node_index, name="Non-negative Matrix Factorization"):
        super().__init__(node_index, name)
        self.params = {
            "n_components": 1,
            "init": None,
            "solver": "cd",
            "beta_loss": "frobenius",
            "tol": 0.0001,
            "max_iter": 200,
            "alpha_W": 0.0,
            "alpha_H": 0.0,
            "l1_ratio": 0.0,
            "shuffle": False,
            "random_state": None,
        }
        self.feature_port_id = self.add_input_port("featuredata", [PortType.DATAFRAMEFLOAT, PortType.MODELDATAFRAMEFLOAT], "Feature Data")
        self.fit_data_port_id = self.add_output_port("fitdata_components", PortType.MODELDATAFRAMEFLOAT, "NMF Components")
        self.loadings_port_id = self.add_output_port("fitdata_loadings", PortType.MODELDATAFRAMEFLOAT, "NMF Loadings")
        self.labels_port_id = self.add_output_port("fitdata_labels", PortType.DATASERIESSTRING, "Component Labels")
    

    def get_input_data(self):
        ret_data = {}
        for port in self.input_ports:
            key = port.connection
            if key in port.value:
                ret_data[port.port_id] = port.value[key]
        feature_data = ret_data.get(self.feature_port_id, None)

        return feature_data

    def compute(self):
        print(f"[{self.node_id}] Computing NMF...")
        feature_data = self.get_input_data()
        if feature_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")
        try:
            feature_data = np.array(feature_data)
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)

            nmf = NMF(
                n_components=self.params["n_components"],
                init=self.params["init"],
                solver=self.params["solver"],
                beta_loss=self.params["beta_loss"],
                tol=self.params["tol"],
                max_iter=self.params["max_iter"],
                alpha_H=self.params["alpha_H"],
                alpha_W=self.params["alpha_W"],
                l1_ratio=self.params["l1_ratio"],
                random_state=self.params["random_state"],
                shuffle=self.params["shuffle"],
                verbose=0,
            )
            nmf.fit(feature_data)
            nmf_components = nmf.transform(feature_data)
            nmf_loadings = nmf.components_.transpose()
            nmf_labels = [f"Cmp {i+1}" for i in range(nmf.n_components)]

            for port in self.output_ports:
                if port.port_id == self.fit_data_port_id:
                    port.value[self.fit_data_port_id] = nmf_components
                elif port.port_id == self.loadings_port_id:
                    port.value[self.loadings_port_id] = nmf_loadings
                elif port.port_id == self.labels_port_id:
                    port.value[self.labels_port_id] = nmf_labels
        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing NMF: {e}")

        return True
    
