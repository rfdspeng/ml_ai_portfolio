# ───────────────────────────────
# src/experiment_runner.py
# ───────────────────────────────
import os
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
from src.utils import load_titanic_data, EXPERIMENTS_DIR
from src.custom_model_selection import custom_cross_validate
from sklearn.model_selection import LearningCurveDisplay
import matplotlib.pyplot as plt


def make_output_dir(experiment_name):
    out_dir = EXPERIMENTS_DIR / experiment_name
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def run_cross_validation(config, custom=False):
    X, y, _ = load_titanic_data()
    
    pipeline = config["ml_pipe"]
    cv = config["splitter"]

    experiments_subdir = make_output_dir(config["experiment_name"])

    if not custom:
        print("Running cross-validation.")
        cv_results = cross_validate(pipeline, X, y=y, cv=cv, return_train_score=True)
        pd.DataFrame(cv_results).to_csv(experiments_subdir / "cv_results.csv", index=False)
        print(f"Finished cross-validation. Results saved to {str(experiments_subdir / "cv_results.csv")}.")
    else:
        print("Running custom cross-validation.")
        [cv_df_out, cv_metrics] = custom_cross_validate(pipeline, X, y, cv)
        cv_df_out.to_csv(experiments_subdir / "ccv_results.csv", index=False)
        with open(experiments_subdir / "ccv_metrics.json", "w") as f:
            json.dump(cv_metrics, f)
        print(f"Finished custom cross-validation. Results saved to {str(experiments_subdir / "ccv_results.csv")}.")

def run_learning_curve(config):
    X, y, _ = load_titanic_data()

    pipeline = config["ml_pipe"]
    cv = config["splitter"]

    experiments_subdir = make_output_dir(config["experiment_name"])

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6), sharey=True)

    common_params = {
        "X": X,
        "y": y,
        "train_sizes": np.linspace(0.1, 1.0, 5),
        "cv": cv,
        "score_type": "both",
        # "n_jobs": 4,
        "line_kw": {"marker": "o"},
        "std_display_style": "fill_between",
        "score_name": "Accuracy",
    }

    print("Generating learning curve.")
    LearningCurveDisplay.from_estimator(pipeline, **common_params, ax=ax)
    handles, label = ax.get_legend_handles_labels()
    ax.legend(handles[:2], ["Training Score", "Test Score"])
    ax.set_title(f"Learning Curve for {config["experiment_name"]}")
    ax.grid()
    fig.savefig(experiments_subdir / "learning_curve.png", dpi=300)
    print(f"Finished generating learning curve. Results saved to {str(experiments_subdir / "learning_curve.png")}.")

def run_hyperparameter_tuning(config, search_type="grid"):
    X, y, _ = load_titanic_data()

    pipeline = config["ml_pipe"]
    cv = config["splitter"]

    experiments_subdir = make_output_dir(config["experiment_name"])

    if search_type == "grid":
        hp_searcher = GridSearchCV(
            pipeline,
            param_grid=config["param_grid"],
            scoring=config.get("scoring", "accuracy"),
            cv=cv,
            return_train_score=True,
        )
    print(f"Running {search_type} search.")
    hp_searcher.fit(X, y)

    pd.DataFrame(
        {"Run": list(range(len(hp_searcher.cv_results_["mean_train_score"]))),
         "Train (Mean)": (np.array(hp_searcher.cv_results_["mean_train_score"])*100).round(2),
         "Train (Std)": (np.array(hp_searcher.cv_results_["std_train_score"])*100/np.sqrt(cv.n_splits)).round(2),
         "Test (Mean)": (np.array(hp_searcher.cv_results_["mean_test_score"])*100).round(2),
         "Test (Std)": (np.array(hp_searcher.cv_results_["std_test_score"])*100/np.sqrt(cv.n_splits)).round(2),
         "Params": hp_searcher.cv_results_["params"]
         }
         ).to_csv(experiments_subdir / f"{search_type}_results.csv", index=False)
    print(f"Finished {search_type} search. Results saved to {str(experiments_subdir / f"{search_type}_results.csv")}.")

def run_training(config):
    X, y, _ = load_titanic_data()

    pipeline = config["ml_pipe"]

    experiments_subdir = make_output_dir(config["experiment_name"])

    print("Training ML pipeline.")
    pipeline.fit(X, y)
    joblib.dump(pipeline, experiments_subdir / "ml_pipeline.joblib")
    print(f"Finished training pipeline. Saved pipeline to {str(experiments_subdir / "ml_pipeline.joblib")}.")

def run_predictions(config):
    experiments_subdir = EXPERIMENTS_DIR / config["experiment_name"]
    model_path = config.get("model_path", experiments_subdir / "ml_pipeline.joblib")
    print(f"Loading model from {model_path}.")
    model = joblib.load(model_path)
    _, _, X_test = load_titanic_data(load_test=True)
    print("Running predictions.")
    y_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)
    print(f"Finished predictions. Predicted survival rate = {sum(y_pred)/len(y_pred)}.")

    # Submission
    pd.DataFrame({"PassengerId": X_test["PassengerId"], "Survived": y_pred}).to_csv(experiments_subdir / "submission.csv", index=False)

    # Save predictions and probabilities for analysis
    df = X_test.copy()
    df["Prediction"] = y_pred
    df["Probability"] = y_proba[:, 1]
    df.to_csv(experiments_subdir / "test_predictions.csv", index=False)
    print(f"Saved results to {str(experiments_subdir / "submission.csv")}, {str(experiments_subdir / "test_predictions.csv")}.")