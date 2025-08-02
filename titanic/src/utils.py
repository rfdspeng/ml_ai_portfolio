from pathlib import Path
import pandas as pd

data_paths = {
    "train": "dataset/train.csv",
    "test": "dataset/test.csv",
    "submit": "dataset/submission.csv",
    "train_extracted": "dataset/train_extracted.csv",
    "test_extracted": "dataset/test_extracted.csv",
}

def find_project_root(anchor_files=("requirements.txt",)) -> str:
    """Walk up the file system until we find a known anchor (like .git or pyproject.toml)."""
    path = Path(__file__).resolve()
    for parent in path.parents:
        if any((parent / anchor).exists() for anchor in anchor_files):
            return str(parent)
    raise RuntimeError("Project root not found. Please make sure an anchor file like 'requirements.txt' exists.")

def load_titanic_data(extracted=False):
    path = Path(find_project_root())
    if not extracted:
        data = {
            "train": pd.read_csv(path / Path(data_paths["train"])),
            "test": pd.read_csv(path / Path(data_paths["test"])),
        }
    else:
        try:
            data = {
                "train": pd.read_csv(path / Path(data_paths["train_extracted"])),
                "test": pd.read_csv(path / Path(data_paths["test_extracted"])),
            }
        except FileNotFoundError:
            print("Extracted dataset not found. Please run src.custom_transformers.feature_extraction()")
            raise
    
    return data