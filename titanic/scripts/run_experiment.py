# ───────────────────────────────
# scripts/run_experiment.py
# ───────────────────────────────
import argparse
import yaml
from src.experiment_runner import run_grid_search, run_cross_validation, predict_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    task_type = config.get("task_type")

    if task_type == "grid_search":
        run_grid_search(config)
    elif task_type == "cross_validate":
        run_cross_validation(config)
    elif task_type == "predict_test":
        predict_test(config)
    else:
        raise ValueError(f"Unknown task_type: {task_type}")

if __name__ == "__main__":
    main()