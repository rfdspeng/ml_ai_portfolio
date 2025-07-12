import pandas as pd
import numpy as np

EXPERIMENT_CONFIG = {
    # "age_strategy": "group_median",
    "age_strategy": False,
    "use_cabin": False,
    "use_embarked": False,
    "log_transform_fare": False,
    "model": "RandomForest",
    "model_params": {"max_depth": 10, "n_estimators": 100, "random_state": 0}
    # "model_params": {"max_leaf_nodes": 80, "n_estimators": 100}
}

def prepare_dataframe(
    df,
    age_strategy="group_median",
    use_cabin=True,
    use_embarked=False,
    log_transform_fare=False,
    is_train=True,
    group_medians=None
):
    df = df.copy()

    if log_transform_fare:
        df["Fare"] = np.log10(df["Fare"]+1)

    # Process Title from Name
    # df["Title"] = df["Name"].map(lambda x: x.strip().split(",")[1].strip().split()[0])

    # if is_train:
    #     # Group rare titles
    #     titles_small_samples = df["Title"].value_counts().index[df["Title"].value_counts() < 10]
    #     df.loc[(df["Title"].isin(titles_small_samples)) & \
    #         (df["Sex"] == "female") & (df["Age"] <= 30), "Title"] = "Miss."
    #     df.loc[(df["Title"].isin(titles_small_samples)) & \
    #         (df["Sex"] == "female") & (df["Age"] > 30), "Title"] = "Mrs."
    #     df.loc[(df["Title"].isin(titles_small_samples)) & \
    #         (df["Sex"] == "male") & (df["Age"] > 12), "Title"] = "Mr."
    #     df.loc[(df["Title"] == "Dr.") & (df["Sex"] == "male"), "Title"] = "Mr."

    df["TotalFam"] = df["SibSp"] + df["Parch"]
    famgroups = df["TotalFam"].map(lambda x: x if x <= 2 else 3)

    # Age handling
    if age_strategy == "group_median":
        df["AgeMissing"] = df["Age"].isna().astype(int)

        if is_train:
            # compute group medians and store them
            df["GroupKey"] = list(zip(df["Title"], df["Pclass"], famgroups))
            group_medians = df.groupby("GroupKey")["Age"].median().to_dict()
        else:
            df["GroupKey"] = list(zip(df["Title"], df["Pclass"], famgroups))
            if group_medians is None:
                raise ValueError("Must provide group_medians during inference.")

        # fill missing ages using group medians
        df["Age"] = df.apply(
            lambda row: group_medians.get(row["GroupKey"], np.nan) if pd.isna(row["Age"]) else row["Age"],
            axis=1
        )

        df = df.drop("GroupKey", axis=1)

    # Cabin handling
    if use_cabin:
        df["CabinLetter"] = df["Cabin"].str[0].fillna("M")
        if is_train:
            df["CabinLetter"] = df["CabinLetter"].replace("T", "C")

    if not use_embarked and "Embarked" in df.columns:
        df = df.drop("Embarked", axis=1)

    # Drop unused
    drop_cols = ["PassengerId", "Ticket", "Name", "Cabin", "SibSp", "Parch"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    return df, group_medians

df = pd.read_csv("./dataset/train.csv")
df, group_medians = prepare_dataframe(df, **{k: v for k, v in EXPERIMENT_CONFIG.items() if k in ["age_strategy", "use_cabin", "use_embarked", "log_transform_fare"]})

# Encoding
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

X = df.drop("Survived", axis=1)
y = df["Survived"].to_numpy()

ord_features = ["Sex"]
if "CabinLetter" in X.columns:
    ord_features.append("CabinLetter")
    # ord_features = ["CabinLetter"]
onehot_features = []
if "Title" in X.columns:
    onehot_features.append("Title")
if "Embarked" in X.columns:
    onehot_features.append("Embarked")
num_features = X.select_dtypes(exclude=["object"]).columns

preprocessor = ColumnTransformer([
    ("num", "passthrough", num_features),
    ("ord", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), ord_features),
    ("onehot", OneHotEncoder(handle_unknown="infrequent_if_exist"), onehot_features)
])

model = RandomForestClassifier(**EXPERIMENT_CONFIG["model_params"])
# model = RandomForestClassifier()

pipeline = Pipeline([
    ("prep", preprocessor),
    ("model", model)
])

from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import make_scorer, f1_score

# f1 = cross_val_score(pipeline, X, y, cv=5, scoring=make_scorer(f1_score)).mean()
scores = cross_validate(pipeline, X, y, scoring=["accuracy", "f1", "f1_macro"], cv=10, return_train_score=True, return_estimator=True)

print(f"{"-"*50}\nScores\n{"-"*50}")
for k in sorted(scores.keys()):
    if k.startswith("test") or k.startswith("train"):
        print(f"{k + " avg, std":30}: {(scores[k].mean()*100).round(1)}, {(scores[k].std()*100).round(1)}")

if hasattr(scores["estimator"][0].named_steps.model, "feature_importances_"):
    print(f"{"-"*50}\nFeature importances\n{"-"*50}")
    feature_importances = (np.concatenate([e.named_steps.model.feature_importances_[:, np.newaxis] for e in scores["estimator"]], axis=1).mean(axis=1)*100).round(1)
    feature_names = scores["estimator"][0].named_steps.prep.get_feature_names_out()[feature_importances.argsort()[::-1]]
    feature_importances = feature_importances[feature_importances.argsort()[::-1]]
    print(*[f"{i[0]:30}: {i[1]}" for i in zip(feature_names, feature_importances)], sep="\n")

# # Optional: log results
# EXPERIMENT_CONFIG["f1_score"] = f1
# with open("experiment_log.json", "a") as f:
#     import json
#     f.write(json.dumps(EXPERIMENT_CONFIG) + "\n")

# pipeline.fit(X, y)

# df_test = pd.read_csv("./dataset/test.csv")
# passenger_ids = df_test.loc[:, "PassengerId"]

# df_test, _ = prepare_dataframe(df_test, is_train=False, group_medians=group_medians, 
#                                **{k: v for k, v in EXPERIMENT_CONFIG.items() if k in ["age_strategy", "use_cabin", "use_embarked"]})

# y_pred = pipeline.predict(df_test)

# output = pd.DataFrame({"PassengerId": passenger_ids, "Survived": y_pred})

# output.to_csv("./dataset/submission.csv", index=False)