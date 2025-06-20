import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import f1_score

# Skip missing or not
# Encoding - different types
# Cross validation
# Probably can wrap the pipeline in another estimator for tuning? Or can tune pipeline itself?
# Different models?
# Don't forget to weight

df_train = pd.read_csv("./dataset/train.csv")

data_pipe = ColumnTransformer([
    ("scaler_only", StandardScaler(), ["Fare", "Age", "SibSp", "Parch"]),
    ("ordinal_encoder", OrdinalEncoder(), ["Sex"]),
    ("onehot_encoder", OneHotEncoder(), ["Embarked", "Pclass"]),
    # ("labels", "passthrough", ["Survived"])
])

df_train_transformed = data_pipe.fit_transform(df_train)

n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=0)

# X = df_train_transformed.drop("Survived", axis="columns")
# y = df_train_transformed["Survived"].copy()
X = df_train_transformed
y = df_train["Survived"].to_numpy()

# model = LogisticRegression()
model = DecisionTreeClassifier()
# model = RandomForestClassifier()
# model = RandomForestClassifier(class_weight="balanced")
# model = RandomForestClassifier(class_weight="balanced_subsample")
# model = HistGradientBoostingClassifier()

f1_train = np.zeros(n_splits)
f1_val = np.zeros(n_splits)
for i, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    X_fold = X[train_idx, :]
    y_fold = y[train_idx]
    model.fit(X_fold, y_fold)
    y_pred = model.predict(X_fold)
    f1_train[i] = f1_score(y_fold, y_pred)

    X_fold = X[val_idx, :]
    y_fold = y[val_idx]
    y_pred = model.predict(X_fold)
    f1_val[i] = f1_score(y_fold, y_pred)

f1_train_avg = f1_train.mean()
f1_val_avg = f1_val.mean()

print(f"f1 train = {f1_train_avg}")
print(f"f1 val = {f1_val_avg}")