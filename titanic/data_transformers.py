import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import f1_score
from typing import Callable, Any
from pandas.core.frame import DataFrame

# Skip missing or not
# Encoding - different types
# Cross validation
# Probably can wrap the pipeline in another estimator for tuning? Or can tune pipeline itself?
# Different models?
# Don't forget to weight
# Which samples are misclassified?
# f1 score - is this calculated for the positive class only?
# Overfitting is because of noise - not capturing the real patterns in the data - you're capturing the noise. Clean data, collect more data (reduce noise)
# Underfitting is because your model is too simply to capture any patterns
# Tree-based models can handle missing values, but how do they do it? Can performance improve if you fill in the values anyway?


class FeatureEng(BaseEstimator, TransformerMixin):
    def __init__(self, skip=True):
        self.skip = skip

    def fit(self, X, y=None):
        return self
    
    def transform(self, X: DataFrame):
        if not self.skip:
            X = X.copy()

            X["TotalFam"] = X["Parch"] + X["SibSp"]
            X["HasFam"] = X["TotalFam"] > 0
            X["AgeLessThanEqual5"] = X["Age"] <= 5
            X["FareLessThanEqual10"] = X["Fare"] <= 10

        return X

df_train = pd.read_csv("./dataset/train.csv")

X = df_train.drop("Survived", axis="columns")
y = df_train["Survived"].to_numpy()

# model = LogisticRegression()
# model = SVC()
model = DecisionTreeClassifier(max_depth=5, max_leaf_nodes=150, random_state=0)
# model = DecisionTreeClassifier()
# model = RandomForestClassifier()
# model = RandomForestClassifier(class_weight="balanced")
# model = RandomForestClassifier(class_weight="balanced_subsample")
# model = HistGradientBoostingClassifier()



data_pipe = ColumnTransformer([
    ("scaler_only", StandardScaler(), ["Fare", "Age", "SibSp", "Parch", "TotalFam"]),
    # ("scaler_only", StandardScaler(), ["Fare", "Age"]),
    # ("ordinal_encoder", OrdinalEncoder(), ["Sex", "Pclass"]),
    # ("onehot_encoder", OneHotEncoder(), ["Embarked", "Pclass"]),
    # ("onehot_encoder", OneHotEncoder(), ["Pclass"]),
    # ("labels", "passthrough", ["Survived"])
    ("ordinal_encoder", OrdinalEncoder(), ["Sex", "Pclass", "HasFam", "AgeLessThanEqual5", "FareLessThanEqual10"])
], remainder="drop")

ml_pipe = Pipeline([
    ("feature_eng", FeatureEng(skip=False)),
    ("preprocess", data_pipe),
    ("model", model)
])

# print(X.columns)
# scores = cross_validate(ml_pipe, X, y, scoring="f1", cv=10, n_jobs=-1, return_train_score=True, return_estimator=True) # bad descriptor failure when debugging
scores = cross_validate(ml_pipe, X, y, scoring="f1", cv=10, return_train_score=True, return_estimator=True)

print(f"{"-"*50}\nScores\n{"-"*50}")
print(f"{"Train score avg, std":30}: {(scores["train_score"].mean()*100).round(1)}, {(scores["train_score"].std()*100).round(1)}")
print(f"{"Val score avg, std":30}: {(scores["test_score"].mean()*100).round(1)}, {(scores["test_score"].std()*100).round(1)}")



print(f"{"-"*50}\nModel learned parameters\n{"-"*50}")
if hasattr(scores["estimator"][0].named_steps.model, "get_depth"):
    print(f"{"Depth":30}: {", ".join([str(e.named_steps.model.get_depth()) for e in scores["estimator"]])}")

if hasattr(scores["estimator"][0].named_steps.model, "get_n_leaves"):
    print(f"{"Number of leaf nodes":30}: {", ".join([str(e.named_steps.model.get_n_leaves()) for e in scores["estimator"]])}")



if hasattr(scores["estimator"][0].named_steps.model, "feature_importances_"):
    print(f"{"-"*50}\nFeature importances\n{"-"*50}")
    feature_importances = (np.concatenate([e.named_steps.model.feature_importances_[:, np.newaxis] for e in scores["estimator"]], axis=1).mean(axis=1)*100).round(1)
    feature_names = scores["estimator"][0].named_steps.preprocess.get_feature_names_out()[feature_importances.argsort()[::-1]]
    feature_importances = feature_importances[feature_importances.argsort()[::-1]]
    print(*[f"{i[0]:30}: {i[1]}" for i in zip(feature_names, feature_importances)], sep="\n")