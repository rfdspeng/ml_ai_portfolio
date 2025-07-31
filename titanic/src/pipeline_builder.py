# ───────────────────────────────
# src/pipeline_builder.py
# ───────────────────────────────
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from src.custom_transformers import TitleExtractor, FareImputer


def build_pipeline(use_title=True, use_fare=True, model="rf"):
    steps = []
    if use_title:
        steps.append(("title", TitleExtractor()))
    if use_fare:
        steps.append(("fare", FareImputer()))

    if model == "rf":
        clf = RandomForestClassifier(random_state=42)
    elif model == "lr":
        clf = LogisticRegression(max_iter=1000)
    else:
        raise ValueError(f"Unsupported model: {model}")

    steps.append(("clf", clf))
    return Pipeline(steps)