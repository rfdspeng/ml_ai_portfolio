from pathlib import Path
import pandas as pd
from sklearn.pipeline import Pipeline
from src.custom_transformers import DynamicDataPrepPipeline
from sklearn.preprocessing import KBinsDiscretizer, QuantileTransformer, PowerTransformer, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, RandomForestRegressor
from sklearn.model_selection import StratifiedKFold
from src.custom_model_selection import make_stratified_k_fold_with_custom_strata
from xgboost import XGBClassifier

def find_project_root(anchor_files=("requirements.txt",)) -> Path:
    """Walk up the file system until we find a known anchor (like .git or pyproject.toml)."""
    path = Path(__file__).resolve()
    for parent in path.parents:
        if any((parent / anchor).exists() for anchor in anchor_files):
            return parent
    raise RuntimeError("Project root not found. Please make sure an anchor file like 'requirements.txt' exists.")

ROOT = find_project_root()

DATA_DIR = ROOT / "dataset"
EXPERIMENTS_DIR = ROOT / "experiments"
OUTPUT_DIR = ROOT / "outputs"

DATA_PATHS = {
    "train": DATA_DIR / "train.csv",
    "test": DATA_DIR / "test.csv",
    "submit": DATA_DIR / "submission.csv",
    "train_extracted": DATA_DIR / "train_extracted.csv",
    "test_extracted": DATA_DIR / "test_extracted.csv",
}

def load_titanic_data(extracted=False):
    path = Path(find_project_root())
    if not extracted:
        data = {
            "train": pd.read_csv(path / Path(DATA_PATHS["train"])),
            "test": pd.read_csv(path / Path(DATA_PATHS["test"])),
        }
    else:
        try:
            data = {
                "train": pd.read_csv(path / Path(DATA_PATHS["train_extracted"])),
                "test": pd.read_csv(path / Path(DATA_PATHS["test_extracted"])),
            }
        except FileNotFoundError:
            print("Extracted dataset not found. Please run src.custom_transformers.feature_extraction()")
            raise
    
    return data

REGISTRY = {
    # Data prep
    "Pipeline": Pipeline,
    "DynamicDataPrepPipeline": DynamicDataPrepPipeline,
    "KBinsDiscretizer": KBinsDiscretizer, 
    "QuantileTransformer": QuantileTransformer, 
    "PowerTransformer": PowerTransformer, 
    "MinMaxScaler": MinMaxScaler,

    # Models
    "LogisticRegression": LogisticRegression,
    "SVC": SVC,
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
    "HistGradientBoostingClassifier": HistGradientBoostingClassifier,
    "XGBClassifier": XGBClassifier,

    # Model selection
    "StratifiedKFold": StratifiedKFold,
    "make_stratified_k_fold_with_custom_strata": make_stratified_k_fold_with_custom_strata,
}

def build_estimators(config):
    estimators = {}
    for key in config:
        estimators[key] = build_estimator(config[key])
    return estimators

def build_estimator(config):
    cls = REGISTRY[config["type"]]
    if config["type"] == "Pipeline":
        steps = []
        for step in config["steps"]:
            step_name = step["name"]
            transformer = build_estimator(step["transformer"])
            steps.append((step_name, transformer))
        return cls(steps)
    else:
        return cls(**config.get("params", {}))