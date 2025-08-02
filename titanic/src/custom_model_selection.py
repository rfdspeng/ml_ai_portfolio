import numpy as np
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

def make_stratified_k_fold_with_custom_strata(X: DataFrame, columns: list[str], n_splits=10, shuffle=True, random_state=0):
    """
    Concatenate values across multiple columns in the input DataFrame
    Create cross-validation splits stratified across the concatenated values

    e.g. columns should be of the form [col1_name, col2_name, ...]
    """
    if not columns:
        raise Exception("make_stratified_k_fold_with_custom_strata: columns cannot be empty")
    
    cv_splitter = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state) # n_splits, shuffle, random_state

    y_concat = make_custom_strata(X, columns)
    
    return cv_splitter.split(X, y_concat) # Generator object. Iterating yields (train_indices, val_indices) (a 2-ple of numpy arrays)

def custom_cross_validate(estimator, X: DataFrame, y: Series | np.ndarray, cv, cv_kwargs={}) -> tuple[DataFrame, dict]:
    # Copy and reset X for indexing alignment
    X_out = X.copy().reset_index(drop=True)

    # Preallocate prediction columns
    X_out["PredictProba"] = np.nan
    X_out["Prediction"] = np.nan

    # Ensure y is a NumPy array for consistent indexing
    y = np.asarray(y)
    
    # Use provided splitter or create StratifiedKFold
    try:
        cv_iter = iter(cv)
    except:
        if hasattr(cv, 'split'):
            splitter = cv
        else:
            splitter = StratifiedKFold(n_splits=cv, **cv_kwargs)
        
        cv_iter = splitter.split(X_out, y)   

    for train_idx, val_idx in cv_iter:
        X_train, y_train = X_out.iloc[train_idx], y[train_idx]
        X_val = X_out.iloc[val_idx]

        estimator.fit(X_train, y_train)

        # Predict class 1 probability and class label
        X_out.loc[val_idx, "PredictProba"] = estimator.predict_proba(X_val)[:, 1]
        X_out.loc[val_idx, "Prediction"] = estimator.predict(X_val)

    # Confusion matrix labels
    y_true = y
    # y_pred = X_out["Prediction"].astype(int)  # ensure consistent type
    y_pred = X_out["Prediction"]

    X_out["CM"] = np.select(
        [
            (y_true == 0) & (y_pred == 0),
            (y_true == 1) & (y_pred == 1),
            (y_true == 0) & (y_pred == 1),
            (y_true == 1) & (y_pred == 0),
        ],
        ["TN", "TP", "FP", "FN"],
        default=""
    )

    # Compute metrics safely
    cm_counts = X_out["CM"].value_counts()
    n = cm_counts.sum()

    # Safely get each component (defaults to 0 if missing)
    TP = cm_counts.get("TP", 0)
    TN = cm_counts.get("TN", 0)
    FP = cm_counts.get("FP", 0)
    FN = cm_counts.get("FN", 0)

    acc = (TP + TN) / n if n > 0 else np.nan
    rec = TP / (TP + FN) if (TP + FN) > 0 else np.nan
    prec = TP / (TP + FP) if (TP + FP) > 0 else np.nan
    f1 = 2 * rec * prec / (rec + prec) if (rec + prec) > 0 else np.nan

    metrics = {
        "accuracy": acc,
        "recall": rec,
        "precision": prec,
        "f1": f1
    }

    X_out["Survived"] = y

    return X_out, metrics