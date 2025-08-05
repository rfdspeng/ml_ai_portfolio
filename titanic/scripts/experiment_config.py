# config = {
#     "ml_pipe": {
#         "type": "Pipeline",
#         "steps": [
#             {
#                 "name": "data_prep",
#                 "transformer": {
#                     "type": "DynamicDataPrepPipeline",
#                     "params": {
#                         "ordinal_columns": ["Sex"],
#                         "numeric_columns": ["Age", "Pclass", "Fare"],
#                         "extract_title": True,
#                         "extract_fam": True,
#                         "extract_deck": True,
#                         "extract_sexpclassage": True,
#                     }
#                 }
#             },
#             {
#                 "name": "model",
#                 "transformer": {
#                     "type": "RandomForestClassifier",
#                     "params": {
#                         "max_depth": 20,
#                         "random_state": 0,
#                     }
#                 }
#             }
#         ]
#     },
#     "splitter": {
#         "type": "StratifiedKFold",
#         "params": {
#             "n_splits": 10,
#             "shuffle": True,
#             "random_state": 0,
#         }
#     }
# }

# config = {
#     "experiment_name": "000_example",
#     "data_prep": {
#         "type": "DynamicDataPrepPipeline",
#         "params": {
#             "ordinal_columns": ["Sex"],
#             "numeric_columns": ["Age", "Pclass", "Fare"],
#             "extract_title": True,
#             "extract_fam": True,
#             "extract_deck": True,
#             "extract_sexpclassage": True,
#         }    
#     },
#     "model": {
#         "type": "RandomForestClassifier",
#         "params": {
#             "max_depth": 20,
#             "random_state": 0,
#         }
#     },
#     "splitter": {
#         "type": "StratifiedKFold",
#         "params": {
#             "n_splits": 10,
#             "shuffle": True,
#             "random_state": 0,
#         }
#     }
# }

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
    }
}

# config = {
#     "numeric_transformations": {
#         "Fare": {
#             "type": "Pipeline",
#             "steps": [
#                 {
#                     "name": "bin",
#                     "transformer": {
#                         "type": "KBinDiscretizer",
#                         "params": {
#                             "n_bins": 4,
#                             "encode": "ordinal"
#                         }
#                     }
#                 },
#                 {
#                     "name": "scale",
#                     "transformer": {
#                         "type": "MinMaxScaler"
#                     }
#                 }
#             ]
#         },
#         "Pclass": {
#             "type": "MinMaxScaler"
#         },
#     },
#     "ml_pipe": {
#         "type": "Pipeline",
#         "steps": [
#             {
#                 "name": "data_prep",
#                 "transformer": {
#                     "type": "DynamicDataPrepPipeline",
#                     "params": {
#                         "onehot_columns": ["Sex"],
#                         "numeric_columns": ["Fare", "Pclass"],
#                         "extract_title": True,
#                         "extract_fam": True,
#                         "fam_kwargs": {"max_famsize": 4},
#                     }
#                 }
#             },
#             {
#                 "name": "model",
#                 "transformer": {
#                     "type": "LogisticRegression",
#                 }
#             }
#         ]
#     },
#     "splitter": {
#         "type": "StratifiedKFold",
#         "params": {
#             "n_splits": 10,
#             "shuffle": True,
#             "random_state": 0,
#         }
#     }
# }

# numeric_transformations = {
#     "Fare": Pipeline([("bin", KBinsDiscretizer(n_bins=4, encode="ordinal")), ("scale", MinMaxScaler())]),
#     "Pclass": MinMaxScaler(),
#     # "FamilySize": OneHotEncoder(handle_unknown="ignore")
# }
# data_prep_pipe = DynamicDataPrepPipeline(
#     numeric_columns={"Fare", "Pclass"},
#     numeric_transformations=numeric_transformations,
#     # onehot_columns={"Sex"},
#     extract_fam=True,
#     # fam_kwargs={"max_famsize": 4},
#     fam_kwargs={"max_famsize": 1},
#     extract_title=True
# )
# model = LogisticRegression()