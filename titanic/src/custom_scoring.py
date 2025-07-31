from sklearn.metrics import make_scorer, accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from typing import Literal
import numpy as np

# Per-category scorer
def category_scorer(y_true, y_pred, categories, category,
                 metric_type: Literal["accuracy", "recall", "precision", "f1", "tn", "tp", "fn", "fp"]):
    
    mask = categories == category # e.g. df["Title"] == "Mr"
    if metric_type == "accuracy":
        return accuracy_score(y_true[mask], y_pred[mask])
    if metric_type == "recall":
        return recall_score(y_true[mask], y_pred[mask], zero_division=np.nan)
    if metric_type == "precision":
        return precision_score(y_true[mask], y_pred[mask], zero_division=np.nan)
    if metric_type == "f1":
        return f1_score(y_true[mask], y_pred[mask], zero_division=np.nan)
    
    cm = confusion_matrix(y_true[mask], y_pred[mask], labels=[0,1])
    if metric_type == "tn":
        return cm[0,0]
    if metric_type == "tp":
        return cm[1,1]
    if metric_type == "fn":
        return cm[1,0]
    if metric_type == "fp":
        return cm[0,1]

# Wrapper for make_scorer — it needs only (estimator, X, y)
def make_scorer_wrapper(categories, category, 
                        metric_type: Literal["accuracy", "recall", "precision", "f1", "tn", "tp", "fn", "fp"]):
    
    def scorer(estimator, X, y):
        y_pred = estimator.predict(X)
        return category_scorer(y, y_pred, categories.loc[X.index], category, metric_type)
    
    return scorer