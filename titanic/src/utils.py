from pathlib import Path
import pandas as pd

def find_project_root(anchor_files=("requirements.txt",)) -> Path:
    """Walk up the file system until we find a known anchor (like .git or pyproject.toml)."""
    path = Path(__file__).resolve()
    for parent in path.parents:
        if any((parent / anchor).exists() for anchor in anchor_files):
            return parent.resolve()
    raise RuntimeError("Project root not found. Please make sure an anchor file like 'requirements.txt' exists.")

ROOT = find_project_root()

DATA_DIR = ROOT / "dataset"
EXPERIMENTS_DIR = ROOT / "experiments"
OUTPUT_DIR = ROOT / "outputs"

DATA_PATHS = {
    "train": DATA_DIR / "train.csv",
    "test": DATA_DIR / "test.csv",
    "submit": DATA_DIR / "submission.csv",
    "train_extracted": DATA_DIR / "train_extracted.csv", # features extracted
    "test_extracted": DATA_DIR / "test_extracted.csv",
}

def load_titanic_data(load_X_y=True, extracted=False, load_test=False, target="Survived"):
    suffix = ""
    if extracted:
        suffix = "_extracted"
    
    try:
        train = pd.read_csv(DATA_PATHS["train" + suffix])
    except FileNotFoundError:
        print(f"{DATA_PATHS["train" + suffix]} not found. You may need to run src.custom_transformers.feature_extraction()")
        raise

    if load_X_y:
        X = train.drop(columns=target)
        y = train[target]
    else:
        X = train
        y = None
    
    if load_test:
        try:
            X_test = pd.read_csv(DATA_PATHS["test" + suffix])
        except FileNotFoundError:
            print(f"{DATA_PATHS["test" + suffix]} not found. You may need to run src.custom_transformers.feature_extraction()")
            raise
    else:
        X_test = None
    
    return X, y, X_test