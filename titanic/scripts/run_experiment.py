# ───────────────────────────────
# scripts/run_experiment.py
# ───────────────────────────────
from pathlib import Path
import os
import argparse
import sys
import yaml
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))
cwd = Path(os.getcwd())
from src.experiment_runner import run_cross_validation, run_learning_curve, run_hyperparameter_tuning
from src.config_parser import build_estimators
from src.utils import EXPERIMENTS_DIR

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--config", required=True)
    parser.add_argument("--config", nargs="?", default="scripts/experiment_config.yaml")
    parser.add_argument("--task", required=True, nargs="+")
    args = parser.parse_args()
    # print(args)
    # print(args.config)

    config_filename = root_dir / args.config if args.config == "scripts/experiment_config.yaml" else cwd / args.config
    with open(config_filename, "r") as f:
        config = yaml.safe_load(f)
    print(f"Loaded config from {config_filename}.")
    
    estimators = build_estimators(config)
    print("Built estimators.")
    # print(estimators.keys())

    for task in args.task:
        if task == "cv": # sklearn cross validation
            run_cross_validation(estimators)
        elif task == "ccv": # custom cross validation (return predictions and probabilities per sample)
            run_cross_validation(estimators, custom=True)
        elif task == "lc": # learning curves
            run_learning_curve(estimators)
        # elif task == "cal": # calibration curves
        #     run_calibration_curve(estimators)
        # elif task == "grid": # hyperparameter tuning with grid search
        #     run_hyperparameter_tuning(estimators)
        # elif task == "predict": # predict on test set
        #     run_predictions(estimators)
        else:
            raise ValueError(f"Unknown task_type: {task}")
    
    with open(EXPERIMENTS_DIR / config["experiment_name"] / "config.yaml", "w") as f:
        yaml.dump(config, f, sort_keys=False)
        print(f"Saved config file to {EXPERIMENTS_DIR / config["experiment_name"] / "config.yaml"}.")

if __name__ == "__main__":
    main()