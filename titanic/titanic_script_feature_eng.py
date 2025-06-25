import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import f1_score
from typing import Callable, Any
from pandas.core.frame import DataFrame

# YOU NEED TO PROTOTYPE/ITERATE FASTER

# Skip missing or not
# Encoding - different types
# Cross validation
# Probably can wrap the pipeline in another estimator for tuning? Or can tune pipeline itself?
# Different models?
# Don't forget to weight
# Which samples are misclassified?
# f1 score - is this calculated for the positive class only?
# Overfitting is because of noise - not capturing the real patterns in the data - you're capturing the noise. Clean data, collect more data (reduce noise)
# Underfitting is because your model is too simple to capture any patterns
# Tree-based models can handle missing values, but how do they do it? Can performance improve if you fill in the values anyway? Probably. It's still missing data that could be useful. I think tree-based models handle missing values by skipping them and using other features.

# More scoring metrics, recall, precision, metrics per class
# Which samples are misclassified? Performance on positive samples is definitely worse.
# Random oversampling. Balancing the class weights actually makes things worse.
# Impute missing values
# Can you "visualize" the noise of Age by plotting label vs. scatter plot? Or just reduce the binwidth.
# Now that you know Age, Sex, Fare are most important, can you do boxplot/violin plot for multivariate analysis for these variables?
# Try SVC

# You should only attempt to automate after you have a good feel for the grid you want to search.
# You need to be quicker about prototyping and manual experimentation - this is important in order to automate the search.
# Used raw features first with default options on a few different models.
# DecisionTree seems like a good candidate since you can easily see things like depth and number of leaf nodes, which allows you to regularize.
# Also feature importances to get a sense.
# f1 binary and f1 macro to see if one class is worse than the other.
# Model overfits. Regularize. Model underfits. I think that means data is bad - model captures noise, and then you constrain model so it doesn't pick up noise, and then you can't predict anyway. Need better features.
# For example, when I simplified Age and Fare into 2-category variables, training and validation performance was bad. Underfitting can be due to model or data.
# Can I set pipeline to NOT fit the data (for validation and testing)?

# What is the mathematical definition of an outlier? Is it a function of mean and standard deviation? 
# What is the meaning of mean and standard deviation for non-normal distributions?

# A question for ChatGPT: I'm doing all these experiments and because the dataset size and models are small, I can easily run them over and over. When dataset size is huge, what's the strat?
# Do I take a subsample of the dataset? Start with simple models to get an intuition? Use tree-based models so I can compute feature importance?

# The cross validation score has high standard deviation - maybe this is why your test score is so much worse than validation? Or are you overfitting to the validation set?
# Print out scores per fold?
# Did imputing Age really have no effect on the results? I feel like it should have SOME effect even if DT/RF naturally handle missing values.

# Can I set Pipeline to inference only? So it only calls transform? Yes - Pipeline.transform()

df_train = pd.read_csv("./dataset/train.csv")

X = df_train.drop("Survived", axis="columns")
y = df_train["Survived"].to_numpy()

farebins = np.array([-1,10,20,40,60,80,100,120,140,np.inf])

def farecat(x):
    return np.argmax(x <= farebins)-1

X["FareCat"] = X["Fare"].map(farecat)

X["AgeCat"] = np.floor(np.clip(X["Age"], a_min=None, a_max=55)/5)

X["TotalFam"] = np.clip(X["Parch"] + X["SibSp"], a_min=0, a_max=4)

X["SexEnc"] = OrdinalEncoder().fit_transform(X[["Sex"]])

# X[["AgeCatScale", "FareCatScale", "TotalFamScale", "PclassScale"]] = MinMaxScaler().fit_transform(X[["AgeCat", "FareCat", "TotalFam", "Pclass"]])

# imp = KNNImputer()
# tr = imp.fit_transform(X[["AgeCatScale", "FareCatScale", "TotalFamScale", "PclassScale", "SexEnc"]])
# X["AgeCatScaleImpute"] = pd.Series(tr[:, 0])

# X = X.loc[:, ["AgeCatScaleImpute", "FareCatScale", "TotalFamScale", "PclassScale", "SexEnc"]]
# X = X.loc[:, ["AgeCatScale", "FareCatScale", "TotalFamScale", "PclassScale", "SexEnc"]]
X = X.loc[:, ["AgeCat", "FareCat", "TotalFam", "Pclass", "SexEnc"]]

# model = LogisticRegression()
# model = SVC()
# model = DecisionTreeClassifier()
# model = DecisionTreeClassifier(max_depth=30, max_leaf_nodes=70, random_state=0, class_weight="balanced")
# model = DecisionTreeClassifier(class_weight="balanced")
# model = RandomForestClassifier()
# model = RandomForestClassifier(class_weight="balanced", random_state=0)
model = RandomForestClassifier(class_weight="balanced", max_leaf_nodes=8, random_state=0)

# model = RandomForestClassifier(class_weight="balanced_subsample")
# model = HistGradientBoostingClassifier(class_weight="balanced", max_leaf_nodes=20)

# print(X.columns)
# scores = cross_validate(ml_pipe, X, y, scoring="f1", cv=10, n_jobs=-1, return_train_score=True, return_estimator=True) # bad descriptor failure when debugging
# scores = cross_validate(ml_pipe, X, y, scoring=["f1", "recall", "precision"], cv=10, return_train_score=True, return_estimator=True)
scores = cross_validate(model, X, y, scoring=["accuracy", "f1_macro", "recall_macro", "precision_macro", "f1", "recall", "precision"], cv=10, return_train_score=True, return_estimator=True)

print(f"{"-"*50}\nScores\n{"-"*50}")
for k in sorted(scores.keys()):
    if k.startswith("test") or k.startswith("train"):
        print(f"{k + " avg, std":30}: {(scores[k].mean()*100).round(1)}, {(scores[k].std()*100).round(1)}")

# print(f"{"Train score avg, std":30}: {(scores["train_score"].mean()*100).round(1)}, {(scores["train_score"].std()*100).round(1)}")
# print(f"{"Val score avg, std":30}: {(scores["test_score"].mean()*100).round(1)}, {(scores["test_score"].std()*100).round(1)}")



print(f"{"-"*50}\nModel learned parameters\n{"-"*50}")
# if hasattr(scores["estimator"][0].named_steps.model, "get_depth"):
#     print(f"{"Depth":30}: {", ".join([str(e.named_steps.model.get_depth()) for e in scores["estimator"]])}")

# if hasattr(scores["estimator"][0].named_steps.model, "get_n_leaves"):
#     print(f"{"Number of leaf nodes":30}: {", ".join([str(e.named_steps.model.get_n_leaves()) for e in scores["estimator"]])}")

if hasattr(scores["estimator"][0], "get_depth"):
    print(f"{"Depth":30}: {", ".join([str(e.get_depth()) for e in scores["estimator"]])}")

if hasattr(scores["estimator"][0], "get_n_leaves"):
    print(f"{"Number of leaf nodes":30}: {", ".join([str(e.get_n_leaves()) for e in scores["estimator"]])}")



# if hasattr(scores["estimator"][0].named_steps.model, "feature_importances_"):
#     print(f"{"-"*50}\nFeature importances\n{"-"*50}")
#     feature_importances = (np.concatenate([e.named_steps.model.feature_importances_[:, np.newaxis] for e in scores["estimator"]], axis=1).mean(axis=1)*100).round(1)
#     feature_names = scores["estimator"][0].named_steps.preprocess.get_feature_names_out()[feature_importances.argsort()[::-1]]
#     feature_importances = feature_importances[feature_importances.argsort()[::-1]]
#     print(*[f"{i[0]:30}: {i[1]}" for i in zip(feature_names, feature_importances)], sep="\n")

if hasattr(scores["estimator"][0], "feature_importances_"):
    print(f"{"-"*50}\nFeature importances\n{"-"*50}")
    feature_importances = (np.concatenate([e.feature_importances_[:, np.newaxis] for e in scores["estimator"]], axis=1).mean(axis=1)*100).round(1)
    feature_names = scores["estimator"][0].feature_names_in_[feature_importances.argsort()[::-1]]
    feature_importances = feature_importances[feature_importances.argsort()[::-1]]
    print(*[f"{i[0]:30}: {i[1]}" for i in zip(feature_names, feature_importances)], sep="\n")


# Inference

model.fit(X, y)

df_test = pd.read_csv("./dataset/test.csv")

X = df_test

X["FareCat"] = X["Fare"].map(farecat)

X["AgeCat"] = np.floor(np.clip(X["Age"], a_min=None, a_max=55)/5)

X["TotalFam"] = np.clip(X["Parch"] + X["SibSp"], a_min=0, a_max=4)

X["SexEnc"] = OrdinalEncoder().fit_transform(X[["Sex"]])

# # imp = KNNImputer()
# # tr = imp.fit_transform(X[["AgeCatScale", "FareCatScale", "TotalFamScale", "PclassScale", "SexEnc"]])
# # X["AgeCatScaleImpute"] = pd.Series(tr[:, 0])

passenger_ids = X.loc[:, "PassengerId"]

X = X.loc[:, ["AgeCat", "FareCat", "TotalFam", "Pclass", "SexEnc"]]

y_pred = model.predict(X)

output = pd.DataFrame({"PassengerId": passenger_ids, "Survived": y_pred})

output.to_csv("./dataset/submission.csv", index=False)