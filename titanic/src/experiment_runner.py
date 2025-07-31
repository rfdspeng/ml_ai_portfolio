# ───────────────────────────────
# src/experiment_runner.py
# ───────────────────────────────
import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from src.data_loader import load_titanic_data, load_test_set
from src.pipeline_builder import build_pipeline
from src.utility_functions import custom_cross_validate


def make_output_dir(experiment_name):
    out_dir = os.path.join("experiments", experiment_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def run_grid_search(config):
    X, y = load_titanic_data()
    pipeline = build_pipeline(**config["pipeline_kwargs"])
    
    cv = StratifiedKFold(**config["cv"])
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


def run_cross_validation(config):
    X, y = load_titanic_data()
    pipeline = build_pipeline(**config["pipeline_kwargs"])
    cv = StratifiedKFold(**config["cv"])

    results = custom_cross_validate(
        pipeline, X, y, 
        cv=cv, 
        scoring=config.get("scoring", "accuracy"),
        return_predictions=config.get("save_predictions", False)
    )

    out_dir = make_output_dir(config["experiment_name"])
    results["metrics"].to_csv(os.path.join(out_dir, "metrics.csv"), index=False)
    if config.get("save_predictions", False):
        results["predictions"].to_csv(os.path.join(out_dir, "predictions.csv"), index=False)

    with open(os.path.join(out_dir, "config.yaml"), "w") as f:
        yaml.safe_dump(config, f)


def predict_test(config):
    model = joblib.load(config["model_path"])
    X_test = load_test_set()
    y_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    df = X_test.copy()
    df["pred"] = y_pred
    if config.get("save_probabilities", True):
        for i in range(y_proba.shape[1]):
            df[f"proba_class_{i}"] = y_proba[:, i]

    out_dir = make_output_dir(config["experiment_name"])
    df.to_csv(os.path.join(out_dir, "test_predictions.csv"), index=False)

    with open(os.path.join(out_dir, "config.yaml"), "w") as f:
        yaml.safe_dump(config, f)