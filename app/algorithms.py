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
        self.fit = None
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
        self.model.fit(self.input_data)
        self.fit = self.model.transform(self.input_data)
        if self.input_args.n_components is None:
            self.input_args.n_components = self.fit.shape[1]
        return self.fit
    
    def get_covariance(self):
        return self.model.get_covariance()
    
    def get_reconstruction(self):
        return np.matmul(self.fit, self.model.components_)
    
    def get_sse(self):
        return (np.matmul(self.fit, self.model.components_) - self.input_data)**2
    
    def get_components(self):
        return self.model.components_
    
    def get_fit(self):
        return self.fit
    

if __name__ == "__main__":
    pca_input = PCA_Input(n_components = 3)

    np.random.seed(5)

    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    fig, ax = plt.subplots(1, 1, figsize=(8, 6), tight_layout=True)


    pca = PCA(pca_input, X)
    X = pca()
    x_ax = np.arange(0, X.shape[1])

    ax.plot(X[0], X[1], "o")

    plt.show()