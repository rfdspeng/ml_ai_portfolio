from copy import deepcopy
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, HistGradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import KBinsDiscretizer, QuantileTransformer, PowerTransformer, MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline
from src.custom_transformers import DynamicDataPrepPipeline

REGISTRY = {
    # Data prep
    "Pipeline": Pipeline,
    "DynamicDataPrepPipeline": DynamicDataPrepPipeline,
    "KBinsDiscretizer": KBinsDiscretizer, 
    "QuantileTransformer": QuantileTransformer, 
    "PowerTransformer": PowerTransformer, 
    "MinMaxScaler": MinMaxScaler,
    "StandardScaler": StandardScaler,

    # Classifiers
    "LogisticRegression": LogisticRegression,
    "SVC": SVC,
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
    "HistGradientBoostingClassifier": HistGradientBoostingClassifier,
    "XGBClassifier": XGBClassifier,

    # Regressors
    "RandomForestRegressor": RandomForestRegressor,

    # Model selection
    "KFold": KFold,
    "StratifiedKFold": StratifiedKFold,
}

def build_estimators(configs: dict):
    configs = deepcopy(configs)

    config_names = configs.keys()
    if "experiment_name" not in config_names:
        raise KeyError("configs must contain 'experiment_name' key")
    if "data_prep" not in config_names:
        raise KeyError("configs must contain 'data_prep' key")
    if "model" not in config_names:
        raise KeyError("configs must contain 'model' key")
    if "splitter" not in config_names:
        raise KeyError("configs must contain 'splitter' key")

    configs["data_prep"].setdefault("params", {})

    if "numeric_transformations" in config_names:
        numeric_transformations = {}
        for feature in configs["numeric_transformations"]: # dict of transformations
            numeric_transformations[feature] = build_estimator(configs["numeric_transformations"][feature])
        configs["data_prep"]["params"]["numeric_transformations"] = numeric_transformations
    
    if "onehot_transformations" in config_names:
        onehot_transformations = {}
        for feature in configs["onehot_transformations"]: # dict of transformations
            onehot_transformations[feature] = build_estimator(configs["onehot_transformations"][feature])
        configs["data_prep"]["params"]["onehot_transformations"] = onehot_transformations

    if "ordinal_transformations" in config_names:
        ordinal_transformations = {}
        for feature in configs["ordinal_transformations"]: # dict of transformations
            ordinal_transformations[feature] = build_estimator(configs["ordinal_transformations"][feature])
        configs["data_prep"]["params"]["ordinal_transformations"] = ordinal_transformations

    if "age_imputer_model" in config_names:
        configs["data_prep"]["params"]["age_imputer_model"] = build_estimator(configs["age_imputer_model"])

    data_prep = build_estimator(configs["data_prep"])
    model = build_estimator(configs["model"])
    splitter = build_estimator(configs["splitter"])

    estimators = {
        "ml_pipe": Pipeline([
            ("data_prep", data_prep),
            ("model", model),
        ]),
        "splitter": splitter,
        "experiment_name": configs["experiment_name"]
    }
    return estimators

def build_estimator(config):
    if not isinstance(config, dict):
        return config # strings, integers, lists, etc.
    
    is_estimator = config.get("type", False)
    if not is_estimator:
        raise KeyError("config must contain 'type' key specifying estimator class")

    cls = REGISTRY.get(config["type"], None)
    if cls is None:
        raise KeyError(f"REGISTRY does not contain {config["type"]} class")

    if config["type"] == "Pipeline":
        steps = []
        for step in config["steps"]:
            step_name = step["name"]
            transformer = build_estimator(step["transformer"])
            steps.append((step_name, transformer))
        return cls(steps)
    else:
        return cls(**config.get("params", {}))