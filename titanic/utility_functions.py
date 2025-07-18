from sklearn.model_selection import StratifiedKFold
from pandas.core.frame import DataFrame
from pandas.core.series import Series

def make_custom_strata(X: DataFrame, columns: list[str]):
    if not columns:
        raise Exception("make_custom_strata: columns cannot be empty")

    y = X[columns].astype("string")

    y_concat = y[columns[0]]

    for col in columns[1:]:
        y_concat = y_concat.str.cat(y[col], sep="_", join="left")
    
    y_concat.name = "_".join(columns)
    return y_concat

def make_stratified_k_fold_with_custom_strata(X: DataFrame, columns: list[str], cv_kwargs={}):
    if not columns:
        raise Exception("make_stratified_k_fold_with_custom_strata: columns cannot be empty")
    
    cv_splitter = StratifiedKFold(**cv_kwargs) # n_splits, shuffle, random_state

    y_concat = make_custom_strata(X, columns)
    
    return cv_splitter.split(X, y_concat) # Generator object. Iterating yields (train_indices, val_indices) (a 2-ple of numpy arrays)