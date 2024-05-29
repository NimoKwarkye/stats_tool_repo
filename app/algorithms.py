#region import libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from dataclasses import dataclass
from sklearn import datasets, decomposition

#endregion

@dataclass
class PCA_Input:
    n_components : int = None
    whiten : bool = False
    svd_solver : str = "auto"
    tol : float = 0.0
    iterated_power :  str = "auto"
    n_oversamples : int = 10
    power_iteration_normalizer : str = "auto"
    random_state : int = None

class PCA:
    def __init__(self, pca_args: PCA_Input, input_data):
        self.input_args = pca_args
        self.input_data = input_data
        self.scores = None
        self.loadings = None
        self.model = None


    def __call__(self):
        self.model = decomposition.PCA(n_components=self.input_args.n_components, 
                                    copy=True, whiten=self.input_args.whiten, 
                                    svd_solver=self.input_args.svd_solver, 
                                    tol=self.input_args.tol, 
                                    iterated_power=self.input_args.iterated_power, 
                                    n_oversamples=self.input_args.n_oversamples, 
                                    power_iteration_normalizer=self.input_args.power_iteration_normalizer, 
                                    random_state=self.input_args.random_state)
        self.model = model.fit(input_data)
        self.scores = model.transform(input_data)
    
    def get_covariance():
        return model.get_covariance()
    
    def get_reconstruction():
        return np.matmul(self.scores, self.model.components_)
    
    def get_sse():
        return (np.matmul(self.scores, self.model.components_) - input_data)**2
    
