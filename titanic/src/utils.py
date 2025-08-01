from pathlib import Path

def find_project_root(anchor_files=("requirements.txt",)) -> Path:
    """Walk up the file system until we find a known anchor (like .git or pyproject.toml)."""
    path = Path(__file__).resolve()
    print(path)
    for parent in path.parents:
        if any((parent / anchor).exists() for anchor in anchor_files):
            print(parent)
            return parent
    raise RuntimeError("Project root not found. Please make sure an anchor file like 'requirements.txt' exists.")