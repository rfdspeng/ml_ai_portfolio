# Required keys: 'experiment_name', 'data_prep', 'model', 'splitter'
# Required for hyperparameter tuning: 'param_grid'

CONFIG = {
    "experiment_name": "000_example",
    "data_prep": {
        "type": "DynamicDataPrepPipeline",
        "params": {
            "ordinal_columns": ["Sex"],
            "numeric_columns": ["Age", "Pclass", "Fare"],
            "extract_title": True,
            "extract_fam": True,
            "extract_deck": True,
            "extract_sexpclassage": True,
        }    
    },
    "model": {
        "type": "RandomForestClassifier",
        "params": {
            "max_depth": 20,
            "random_state": 0,
        }
    },
    "splitter": {
        "type": "StratifiedKFold",
        "params": {
            "n_splits": 5,
            "shuffle": True,
            "random_state": 0,
        }
    },
    "numeric_transformations": {
        "Fare": {
            "type": "Pipeline",
            "steps": [
                {
                    "name": "bin",
                    "transformer": {
                        "type": "KBinsDiscretizer",
                        "params": {
                            "n_bins": 4,
                            "encode": "ordinal"
                        }
                    }
                },
                {
                    "name": "scale",
                    "transformer": {
                        "type": "MinMaxScaler"
                    }
                }
            ]
        },
        "Pclass": {
            "type": "MinMaxScaler"
        },
    },
    "age_imputer_model": {
        "type": "RandomForestRegressor",
        "params": {
            "max_depth": 20
        }
    },
    "param_grid": [
        {
            "data_prep__ordinal_columns": [["Sex"]],
            "data_prep__numeric_columns": [["Age", "Pclass", "Fare"]],
            "data_prep__extract_title": [False, True],
            "data_prep__extract_fam": [False, True],
            "data_prep__extract_deck": [False, True],
            "data_prep__extract_sexpclassage": [False, True],
            "model__max_depth": [5, 20],
        },
    ]
}