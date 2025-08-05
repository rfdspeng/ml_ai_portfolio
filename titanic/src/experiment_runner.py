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
        grid = GridSearchCV(
            pipeline,
            config["param_grid"],
            scoring=config.get("scoring", "accuracy"),
            cv=cv,
            return_train_score=True,
            n_jobs=-1,
        )
    grid.fit(X, y)

    out_dir = make_output_dir(config["experiment_name"])
    joblib.dump(grid.best_estimator_, os.path.join(out_dir, "model.pkl"))
    pd.DataFrame(grid.cv_results_).to_csv(os.path.join(out_dir, "cv_results.csv"), index=False)

    with open(os.path.join(out_dir, "metrics.json"), "w") as f:
        json.dump({
            "best_score": grid.best_score_,
            "best_params": grid.best_params_
        }, f, indent=2)

    with open(os.path.join(out_dir, "config.yaml"), "w") as f:
        yaml.safe_dump(config, f)

# def predict_test(config):
#     model = joblib.load(config["model_path"])
#     X_test = load_test_set()
#     y_proba = model.predict_proba(X_test)
#     y_pred = model.predict(X_test)

#     df = X_test.copy()
#     df["pred"] = y_pred
#     if config.get("save_probabilities", True):
#         for i in range(y_proba.shape[1]):
#             df[f"proba_class_{i}"] = y_proba[:, i]

#     out_dir = make_output_dir(config["experiment_name"])
#     df.to_csv(os.path.join(out_dir, "test_predictions.csv"), index=False)

#     with open(os.path.join(out_dir, "config.yaml"), "w") as f:
#         yaml.safe_dump(config, f)