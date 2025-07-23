# 0 - model depth ~ 12
param_grid = [
    {
        "data_prep__numeric_columns": [{"Age", "Pclass", "Fare", "SibSp", "Parch"}],
        "model__max_depth": [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5],
    },
]

# 1 - title alone is the best
param_grid = [
    {
        "data_prep__extract_title": [False, True],
        "data_prep__extract_fam": [False, True],
        "data_prep__extract_deck": [False, True],
        "data_prep__extract_sexpclassage": [False, True],
    },
]

# 2 - reducing valid titles degrades performance, deck degrades performance
param_grid = [
    {
        "data_prep__extract_title": [True],
        "data_prep__title_kwargs": [{"valid": ["Mr", "Miss", "Mrs", "Master", "Rev"]}],
        "data_prep__extract_deck": [False, True],
    },
]

# 3 - SibSp, Parch, FamilySize all degrade performance
param_grid = [
    {
        "data_prep__numeric_columns": [{"Age", "Pclass", "Fare"}, {"Age", "Pclass", "Fare", "SibSp", "Parch"}],
        "data_prep__extract_title": [True],
        "data_prep__title_kwargs": [{}, {"valid": ["Mr", "Miss", "Mrs", "Master", "Rev"]}],
        "data_prep__extract_fam": [True],
        "data_prep__fam_kwargs": [{}, {"max_famsize": 4}]
    },
    {
        "data_prep__numeric_columns": [{"Age", "Pclass", "Fare"}, {"Age", "Pclass", "Fare", "SibSp", "Parch"}],
        "data_prep__extract_title": [True],
        "data_prep__title_kwargs": [{}, {"valid": ["Mr", "Miss", "Mrs", "Master", "Rev"]}],
    },
]

# 4 - depth ~ 8-12
param_grid = [
    {
        "data_prep__extract_title": [True],
        "model__max_depth": [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5],
    },
]

# 5 - remove one at a time: Fare, Sex, Age, Title, Pclass
# param_grid = [
#     {
#         "data_prep__extract_title": [True],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Age", "Pclass", "Fare"}],
#         "data_prep__ordinal_columns": [{"Sex"}],
#     },
#     {
#         "data_prep__extract_title": [True],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Age", "Pclass"}],
#         "data_prep__ordinal_columns": [{"Sex"}],
#     },
#     {
#         "data_prep__extract_title": [True],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Age", "Pclass", "Fare"}],
#         "data_prep__ordinal_columns": [set()],
#     },
#     {
#         "data_prep__extract_title": [True],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Pclass", "Fare"}],
#         "data_prep__ordinal_columns": [{"Sex"}],
#     },
#     {
#         "data_prep__extract_title": [False],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Age", "Pclass", "Fare"}],
#         "data_prep__ordinal_columns": [{"Sex"}],
#     },
#     {
#         "data_prep__extract_title": [True],
#         "model__max_depth": [8],
#         "data_prep__numeric_columns": [{"Age", "Fare"}],
#         "data_prep__ordinal_columns": [{"Sex"}],
#     },
# ]

# 6 - try with both Fare and FareTransformed - seemingly no improvement
param_grid = [
    {
        "data_prep__extract_title": [True],
        "data_prep__transform_fare": [True],
        "data_prep__fare_kwargs": [{}, {"bin": True}],
        "model__max_depth": [10, 9, 8],
        "model__n_estimators": [100, 150],
    },
]

# 7 - no reduction in performance with FareTransformed until you bin. After binning, significantly worse performance.
param_grid = [
    {
        "data_prep__numeric_columns": [{"Age", "Pclass"}],
        "data_prep__extract_title": [True],
        "data_prep__transform_fare": [True],
        "data_prep__fare_kwargs": [{}, {"bin": True}],
        "model__max_depth": [10, 9, 8],
        "model__n_estimators": [100, 150],
    },
]

# 8 - not much difference b/w 100 and 1000
param_grid = [
    {
        "data_prep__numeric_columns": [{"Age", "Pclass"}],
        "data_prep__extract_title": [True],
        "data_prep__transform_fare": [True],
        "model__max_depth": [8, 12, 15],
        "model__n_estimators": [10, 100, 1000],
    },
]

# 9 - when imputing age, add FareTransformed but not Age_Missing
param_grid = [
    {
        "data_prep__numeric_columns": [{"Age", "Pclass"}],
        "data_prep__extract_title": [True],
        "data_prep__transform_fare": [True],
        "model__max_depth": [8],
        "data_prep__age_imputer_model": [RandomForestRegressor(max_depth=10, random_state=0)],
        "data_prep__impute_age_kwargs": [{"add_indicator": True, "feature_names": {"numeric": {"FamilySize", "SibSp", "Pclass", "FareTransformed"}, "ordinal": {"Sex"}, "onehot": {"Title"}}},
                                         {"feature_names": {"numeric": {"FamilySize", "SibSp", "Pclass", "FareTransformed"}, "ordinal": {"Sex"}, "onehot": {"Title"}}},
                                         {"add_indicator": True},
                                         {}]
    },
]