from sklearn.model_selection import StratifiedKFold
from pandas.core.frame import DataFrame
from pandas.core.series import Series

def make_stratified_k_fold_with_custom_strata(X: DataFrame, columns: list[str], kwargs={}):
    if not columns:
        raise Exception("make_stratified_k_fold_with_custom_strata: columns cannot be empty")
    
    cv_splitter = StratifiedKFold(**kwargs) # n_splits, shuffle, random_state

    y = X[columns].astype("string")

    y_concat = y[columns[0]]

    for col in columns[1:]:
        y_concat = y_concat.str.cat(y[col], sep="_", join="left")
    
    return cv_splitter.split(X, y_concat) # Generator object. Iterating yields (train_indices, val_indices) (a 2-ple of numpy arrays)