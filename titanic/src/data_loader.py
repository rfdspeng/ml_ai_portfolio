# src/data_loader.py
import pandas as pd
from sklearn.model_selection import train_test_split

def load_titanic_data(return_X_y=True, as_dataframe=True, include_test=False):
    df = pd.read_csv("data/processed/train.csv")
    X = df.drop(columns="Survived")
    y = df["Survived"]
    if return_X_y:
        return X, y
    else:
        return df
    
def load_test_set():
    return pd.read_csv("data/processed/test.csv")