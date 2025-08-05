from pathlib import Path
import yaml
from experiment_config import CONFIG

# print(Path(__file__).resolve().parent / "experiment_config.yaml")

with open(Path(__file__).resolve().parent / "experiment_config.yaml", "w") as f:
    yaml.dump(CONFIG, f, sort_keys=False)