import pandas as pd
import numpy as np




def read_data_pca(filepath:str, targets:str="", **kwargs):
    df = pd.read_csv(filepath, **kwargs)
    data_targets = None
    if len(targets) > 0:
        data_targets = df[targets].values
    new_columns = [col for col in df.columns if col != targets]
    df = df[new_columns]
    return_data = {
        "data":df.to_numpy(),
        "features": df.columns.values,
        "targets": data_targets,
        "samples": df.index.values
    }

    return return_data

#TODO check for other csv seperated files not work for tabs
if __name__ == '__main__':
    print(read_data_pca("app/data/test.csv", "g", sep='\t'))