import numpy as np
import pandas as pd
from app.core.node import Node
from app.core.port import PortType
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, OPTICS, SpectralClustering


class KMeansNode(Node):
    def __init__(self, node_index, name="KMeans"):
        super().__init__(node_index, name)
        self.params = {
            "n_clusters": 2,
            "init": "k-means++",
            "n_init": "auto",
            "max_iter": 300,
            "tol": 1e-4,
            "verbose": 0,
            "random_state": None,
            "copy_x": True,
            "algorithm": "lloyd",
        }
        self.kmeans = None
        self.feature_port_id = self.add_input_port("featuredata", 
                                                   [PortType.DATAFRAMEFLOAT, 
                                                    PortType.MODELDATAFRAMEFLOAT], 
                                                    "Feature Data", True)
        self.feature_labels_port_id = self.add_input_port("featurelabels", [PortType.FEATURELABELSSTRING], "Feature Labels")
        self.fit_data_port_id = self.add_output_port("kmeansfitdata", PortType.MODELDATAFRAMEFLOAT, "KMeans Fit Data")
        self.fit_centroid_port_id = self.add_output_port("kmeanscentroiddata", PortType.MODELDATAFRAMEFLOAT, "KMeans Centroids")
        self.cluster_labels_port_id = self.add_output_port("kmeansclusterlabels", PortType.TARGETLABELSSTRING, "Cluster Labels")
    
    def pre_save(self):
        data = self.get_output_data()
        input_data = self.get_input_data()
        save_dir = self.compose_dir_name(self.feature_port_id)
        feature_labels = input_data.get(self.feature_labels_port_id)
        fit_data = data.get(self.fit_data_port_id)
        centroids = data.get(self.fit_centroid_port_id)
        labels = data.get(self.cluster_labels_port_id)
        if feature_labels is None:
            feature_labels = ["Feature " + str(i) for i in range(centroids.shape[1])]
        centroids_dict = {
            "clusters": np.unique(labels)
        }
        for i, name in enumerate(feature_labels):
            centroids_dict[name] = centroids[:, i]
        centroids_df = pd.DataFrame(centroids_dict)
        fit_data_dict = {}
        for i, name in enumerate(np.unique(labels)):
            fit_data_dict[name] = fit_data[:, i]
        fit_data_df = pd.DataFrame(fit_data_dict)
        labels_dict = {
            "cluster_labels": labels
        }
        labels_df = pd.DataFrame(labels_dict)
        return save_dir, {"kmeans_centroids": centroids_df, "kmeans_fit_data": fit_data_df, 
                                  "kmeans_labels": labels_df}, {"kmeans_model": self.kmeans}


    def compute(self):
        feature_data = self.get_input_data().get(self.feature_port_id)
        if feature_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)

            self.kmeans = KMeans(
                n_clusters=self.params["n_clusters"],
                init=self.params["init"],
                n_init=self.params["n_init"],
                max_iter=self.params["max_iter"],
                tol=self.params["tol"],
                verbose=self.params["verbose"],
                random_state=self.params["random_state"],
                algorithm=self.params["algorithm"],
                copy_x=self.params["copy_x"],
            )
            self.kmeans.fit(feature_data)
            labels = self.kmeans.predict(feature_data)
            x_transformed = self.kmeans.transform(feature_data)

            return_log = f"inertia: {self.kmeans.inertia_}\niterations: {self.kmeans.n_iter_}\nfeatures seen:{self.kmeans.n_features_in_}\nscore: {self.kmeans.score(feature_data)}"

            output_data ={
                self.fit_data_port_id: x_transformed,
                self.fit_centroid_port_id: self.kmeans.cluster_centers_,
                self.cluster_labels_port_id: labels,
            }
            self.store_data_in_ports(output_data)

            return return_log
            
        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing KMeans: {e}")


class DBSCANNode(Node):
    def __init__(self, node_index, name="DBSCAN"):
        super().__init__(node_index, name)
        self.params = {
            "eps": 0.5,
            "min_samples": 5,
            "metric": "euclidean",
            "algorithm": "auto",
            "leaf_size": 30,
            "n_jobs": None,
        }
        self.dbscan = None
        self.feature_port_id = self.add_input_port("featuredata", 
                                                   [PortType.DATAFRAMEFLOAT, 
                                                    PortType.MODELDATAFRAMEFLOAT], 
                                                    "Feature Data", True)
        self.feature_labels_port_id = self.add_input_port("featurelables", [PortType.DATASERIESFLOAT], "Feature Labels")
        self.fit_data_port_id = self.add_output_port("dbscanfitdata", PortType.MODELDATAFRAMEFLOAT, "DBSCAN Fit Data")
        self.cluster_labels_port_id = self.add_output_port("dbscanclusterlabels", PortType.TARGETLABELSSTRING, "Cluster Labels")


    def pre_save(self):
        data = self.get_output_data()
        save_dir = self.compose_dir_name(self.feature_port_id)
        labels = data.get(self.cluster_labels_port_id)

        labels_dict = {
            "cluster_labels": labels
        }
        labels_df = pd.DataFrame(labels_dict)
        return save_dir, {"dbscan_labels": labels_df}, {"dbscan_model": self.dbscan}
        



    def compute(self):
        feature_data = self.get_input_data().get(self.feature_port_id)
        if feature_data is None:
            raise ValueError(f"[{self.node_id}] Missing input data.")

        try:
            feature_data = np.array(feature_data)
            if feature_data.ndim == 1:
                feature_data = feature_data.reshape(-1, 1)

            self.dbscan = DBSCAN(
                eps=self.params["eps"],
                min_samples=self.params["min_samples"],
                metric=self.params["metric"],
                algorithm=self.params["algorithm"],
                leaf_size=self.params["leaf_size"],
                n_jobs=self.params["n_jobs"],
            )
            labels = self.dbscan.fit_predict(feature_data)
            fit_data = self.dbscan.components_
            
            true_labels = [i for i in labels if i >= 0]
            return_log = f"Number of clusters: {len(np.unique(true_labels))}\nfeatures seen: {self.dbscan.n_features_in_}"
            output_data ={
                self.fit_data_port_id: fit_data,
                self.cluster_labels_port_id: np.array(labels),
            }
            self.store_data_in_ports(output_data)
            return return_log
        except Exception as e:
            raise ValueError(f"[{self.node_id}] Error computing DBSCAN: {e}")