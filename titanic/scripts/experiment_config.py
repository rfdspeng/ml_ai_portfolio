CONFIG = {
    "experiment_name": "004b_age_imputer_cv",
    "data_prep": {
        "type": "DynamicDataPrepPipeline",
        "params": {
            "extract_title": True,
            "extract_fam": True,
            "numeric_columns": ["SibSp", "Pclass", "Fare"],
        }    
    },
    "numeric_transformations": {"default": "passthrough"},
    "model": {
        "type": "RandomForestRegressor",
        "params": {
            "max_depth": 4,
            "n_estimators": 10,
            "random_state": 0,
        }
    },
    "splitter": {
        "type": "KFold",
        "params": {
            "n_splits": 5,
            "shuffle": True,
            "random_state": 0,
        }
    },
    # "param_grid": [
    #     {
    #         "model__max_depth": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    #         "model__n_estimators": [1, 5, 10],
    #     },
    # ],
    "target": "Age"
}