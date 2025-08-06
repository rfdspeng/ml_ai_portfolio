from pathlib import Path
import re
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin, clone
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.utils.validation import check_is_fitted
from src.utils import DATA_PATHS, load_titanic_data

def build_column_transformer(numeric: list[str] | None = None, 
                             numeric_transformations: dict | None = None,
                             onehot: list[str] | None = None, 
                             onehot_transformations: dict | None = None,
                             ordinal: list[str] | None = None,
                             ordinal_transformations: dict | None = None,
                             ) -> ColumnTransformer:
    """ 
    Build a ColumnTransformer from input lists of feature names
    
    """

    numeric = numeric or []
    numeric_transformations = numeric_transformations or {}
    numeric_transformations.setdefault("default", StandardScaler())
    onehot = onehot or []
    onehot_transformations = onehot_transformations or {}
    onehot_transformations.setdefault("default", OneHotEncoder())
    ordinal = ordinal or []
    ordinal_transformations = ordinal_transformations or {}
    ordinal_transformations.setdefault("default", Pipeline([
        ("encode", OrdinalEncoder()),
        ("scale", MinMaxScaler())
        ])
    )

    transformers = []
    for col in numeric:
        transformers.append((f"num_{col}", numeric_transformations.get(col, numeric_transformations.get("default")), [col]))
    for col in ordinal:
        transformers.append((f"ord_{col}", ordinal_transformations.get(col, ordinal_transformations.get("default")), [col]))
    for col in onehot:
        transformers.append((f"onehot_{col}", onehot_transformations.get(col, onehot_transformations.get("default")), [col]))

    return ColumnTransformer(transformers, remainder="drop")

def get_default_encoding(feature):
    """
    Used by DynamicDataPrepPipeline and AgeImputer during fit
    """

    if feature == "Sex":
        return OneHotEncoder(categories=[["male", "female"]], handle_unknown="error")
    elif feature == "Title":
        return OneHotEncoder(categories=[["Mr", "Miss", "Mrs", "Master", "Dr", "Rev", "Unknown"]], handle_unknown="ignore")
    elif feature == "Deck":
        return Pipeline([
            ("encode", OrdinalEncoder(categories=[sorted(["A", "B", "C", "D", "E", "F", "G", "U"], reverse=True)], handle_unknown="error")),
            ("scale", MinMaxScaler())
            ])
    else:
        raise ValueError("Please provide valid feature: 'Sex', 'Title', and 'Deck'.")

class DynamicDataPrepPipeline(BaseEstimator, TransformerMixin):
    def __init__(self, 
                 extract_fam=False, 
                 fam_kwargs: dict | None = None, 
                 extract_title=False, 
                 title_kwargs: dict | None = None,
                 extract_deck=False, 
                 deck_kwargs: dict | None = None,
                 extract_sexpclassage=False, 
                 sexpclassage_kwargs: dict | None = None,
                 age_imputer_model: BaseEstimator | None = None, 
                 impute_age_kwargs: dict | None = None,
                 numeric_columns: list[str] | None = None,
                 numeric_transformations: dict | None = None,
                 onehot_columns: list[str] | None = None,
                 onehot_transformations: dict | None = None,
                 ordinal_columns: list[str] | None = None,
                 ordinal_transformations: dict | None = None
                 ):
        
        self.extract_fam = extract_fam
        self.fam_kwargs = fam_kwargs
        self.extract_title = extract_title
        self.title_kwargs = title_kwargs
        self.extract_deck = extract_deck
        self.deck_kwargs = deck_kwargs
        self.extract_sexpclassage = extract_sexpclassage
        self.sexpclassage_kwargs = sexpclassage_kwargs
        self.age_imputer_model = age_imputer_model
        self.impute_age_kwargs = impute_age_kwargs
        self.numeric_columns = numeric_columns
        self.numeric_transformations = numeric_transformations
        self.onehot_columns = onehot_columns
        self.onehot_transformations = onehot_transformations
        self.ordinal_columns = ordinal_columns
        self.ordinal_transformations = ordinal_transformations
    
    @staticmethod
    def clone_estimator_dict(d: dict) -> dict:
        """
        Input argument is a dictionary
        Each value is either an estimator or an immutable Python type
        This function returns a new dictionary with cloned estimators
        """
        d_copy = {}
        for k, v in d.items():
            try:
                d_copy[k] = clone(v)
            except TypeError:
                d_copy[k] = v
        return d_copy
    
    def fit(self, X: DataFrame, y=None):
        # Instantiate extractors
        fam_kwargs = self.fam_kwargs.copy() if self.fam_kwargs is not None else {}
        fam_kwargs["extract"] = self.extract_fam
        fam = FamilySizeExtractor(**fam_kwargs)

        title_kwargs = self.title_kwargs.copy() if self.title_kwargs is not None else {}
        title_kwargs["extract"] = self.extract_title
        title = TitleExtractor(**title_kwargs)

        deck_kwargs = self.deck_kwargs.copy() if self.deck_kwargs is not None else {}
        deck_kwargs["extract"] = self.extract_deck
        deck = DeckExtractor(**deck_kwargs)

        sexpclassage_kwargs = self.sexpclassage_kwargs.copy() if self.sexpclassage_kwargs is not None else {}
        sexpclassage_kwargs["extract"] = self.extract_sexpclassage
        sexpclassage = SexPclassAgeExtractor(**sexpclassage_kwargs)

        impute_age_kwargs = self.impute_age_kwargs.copy() if self.impute_age_kwargs is not None else {}
        impute_age_kwargs["model"] = clone(self.age_imputer_model) if self.age_imputer_model is not None else None
        age_imputer = AgeImputer(**impute_age_kwargs)

        numeric_columns = self.numeric_columns.copy() if self.numeric_columns is not None else ["Age", "Pclass", "Fare"]
        numeric_transformations = DynamicDataPrepPipeline.clone_estimator_dict(self.numeric_transformations) if self.numeric_transformations is not None else {}

        onehot_columns = self.onehot_columns.copy() if self.onehot_columns is not None else ["Sex"]
        onehot_transformations = DynamicDataPrepPipeline.clone_estimator_dict(self.onehot_transformations) if self.onehot_transformations is not None else {}
        onehot_transformations.setdefault("Sex", get_default_encoding("Sex"))
        onehot_transformations.setdefault("Title", get_default_encoding("Title"))

        ordinal_columns = self.ordinal_columns.copy() if self.ordinal_columns is not None else []
        ordinal_transformations = DynamicDataPrepPipeline.clone_estimator_dict(self.ordinal_transformations) if self.ordinal_transformations is not None else {}
        ordinal_transformations.setdefault("Deck", get_default_encoding("Deck"))

        # Build extractor pipeline
        self.feature_extractor_ = Pipeline([
            ("fare_imputer", FareImputer()),
            ("fam", fam),
            ("title", title),
            ("deck", deck),
            ("age_imputer", age_imputer),
            ("sexpclassage", sexpclassage),
        ])

        # Dynamically choose columns
        numeric = list(set(X.select_dtypes(exclude=["object", "category"]).columns) & set(numeric_columns))
        ordinal = list(set(X.select_dtypes(include=["object", "category"]).columns) & set(ordinal_columns))
        onehot = list(set(X.select_dtypes(include=["object", "category"]).columns) & set(onehot_columns))

        self.feature_names_in_ = numeric.copy()
        self.feature_names_in_.extend(ordinal.copy())
        self.feature_names_in_.extend(onehot.copy())

        if self.extract_fam:
            numeric.append('FamilySize')

        if self.extract_title:
            onehot.append('Title')

        if self.extract_deck:
            ordinal.append('Deck')
        
        if self.extract_sexpclassage:
            onehot.append('SexPclassAge')
        
        if age_imputer.add_indicator:
            ordinal.append("Age_Missing")
        
        self.feature_names_out_ = numeric.copy()
        self.feature_names_out_.extend(ordinal.copy())
        self.feature_names_out_.extend(onehot.copy())

        self.col_tf_ = build_column_transformer(numeric=numeric, 
                                                numeric_transformations=numeric_transformations,
                                                onehot=onehot, 
                                                onehot_transformations=onehot_transformations,
                                                ordinal=ordinal,
                                                ordinal_transformations=ordinal_transformations)

        # Final full pipeline
        self.pipeline_ = Pipeline([
            ("extractor", self.feature_extractor_),
            ("col_tf", self.col_tf_)
        ])

        self.pipeline_.fit(X, y)
        return self

    def transform(self, X):
        check_is_fitted(self)
        return self.pipeline_.transform(X)
    
    def get_feature_names_out(self):
        check_is_fitted(self)
        return self.pipeline_.named_steps["col_tf"].get_feature_names_out()

def feature_extraction():
    pipe = Pipeline([
        ("fam", FamilySizeExtractor()),
        ("title", TitleExtractor()),
        ("deck", DeckExtractor()),
        ("sexpclassage", SexPclassAgeExtractor()),
    ])

    X, _, X_test = load_titanic_data(load_X_y=False, extracted=False, load_test=True)
    X = pipe.transform(X)
    X_test = pipe.transform(X_test)

    X.to_csv(DATA_PATHS["train_extracted"], index=False)
    X_test.to_csv(DATA_PATHS["test_extracted"], index=False)

class ThresholdClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, base_estimator, threshold=0.5, subgroups=None, subgroup_thresholds=None):
        self.base_estimator = base_estimator
        self.threshold = threshold

        # subgroups is a 2-ple
            # First element is a tuple of titles, e.g. ("Mr", "Mrs")
            # Second element is indices of the feature matrix corresponding to the one-hot encoded titles
        self.subgroup_names, self.subgroup_indices = subgroups if subgroups else (None, None)
        self.subgroups = subgroups

        # subgroup_thresholds is a dictionary. Ex: {"Mr": 0.4, "Miss": 0.6}
        if subgroup_thresholds and subgroups:
            self.subgroup_thresholds = np.array([subgroup_thresholds.get(name, threshold) for name in subgroups[0]])[:, np.newaxis]
        else:
            self.subgroup_thresholds = None

    def fit(self, X, y):
        self.base_estimator.fit(X, y)
        self.is_fitted_ = True
        return self

    def predict_proba(self, X):
        check_is_fitted(self)
        return self.base_estimator.predict_proba(X)

    def predict(self, X):
        check_is_fitted(self)
        probs = self.predict_proba(X)[:, 1]
        if (self.subgroup_thresholds is not None) and (self.subgroup_indices is not None):
            return (probs >= (X[:, self.subgroup_indices] @ self.subgroup_thresholds).squeeze()).astype(int)
        else:
            return (probs >= self.threshold).astype(int)

class MLPipeline(BaseEstimator, ClassifierMixin):
    def __init__(self, data_prep_class=DynamicDataPrepPipeline, data_prep_kwargs={}, classifier_class=ThresholdClassifier, classifier_kwargs={}):
        self.data_prep_class = data_prep_class
        self.data_prep_kwargs = data_prep_kwargs
        self.classifier_class = classifier_class
        self.classifier_kwargs = classifier_kwargs
    
    def fit(self, X, y):
        self.data_prep_ = self.data_prep_class(**self.data_prep_kwargs)

        # "Fits" the data prep pipeline - instantiates the individual components based on the constructor parameters
        self.data_prep_.fit(X, y)

        # Look for feature names that include "Title_", e.g. "onehot__Title_Mr"
        # Store as a 2-ple
            # First element is a tuple of titles, e.g. ("Mr", "Mrs")
            # Second element is indices of the feature matrix corresponding to the one-hot encoded titles
        pattern = re.compile(r"Title_([a-zA-Z]+)")
        feature_names = self.data_prep_.get_feature_names_out()
        self.subgroups_ = tuple(zip(*[(title.group(1), index) for index, title in enumerate([pattern.search(f) for f in feature_names]) if title]))

        # Instantiate the classifier with the subgroups
        self.classifier_ = self.classifier_class(**self.classifier_kwargs, subgroups=self.subgroups_)

        self.pipeline_ = Pipeline([
            ("data_prep", self.data_prep_),
            ("clf", self.classifier_)
        ])
        self.pipeline_.fit(X, y)
        return self
    
    def predict(self, X):
        check_is_fitted(self)
        return self.pipeline_.predict(X)
    
    def predict_proba(self, X):
        check_is_fitted(self)
        return self.pipeline_.predict_proba(X)

# Extract family size
class FamilySizeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, extract=True, max_famsize: int | None=None):
        self.extract = extract
        self.max_famsize = max_famsize
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        if self.extract and ("SibSp" in X_out.columns) and ("Parch" in X_out.columns):
            X_out["FamilySize"] = (X_out["SibSp"] + X_out["Parch"]).clip(upper=self.max_famsize)
        return X_out
    
    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.requires_fit = False
        return tags

# Extract titles from names
class TitleExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, extract=True, 
                 to_replace={"Mlle": "Miss", "Mme": "Mrs", "Ms": "Miss"}, 
                 valid=["Mr", "Miss", "Mrs", "Master", "Dr", "Rev"], 
                 fallback="Unknown"):
        self.extract = extract
        self.to_replace = to_replace
        self.valid = valid
        self.fallback = fallback
        self.pattern = re.compile(r"\b([a-zA-Z]+?)\.")

    def _extract_one(self, x) -> str:
        if isinstance(x, str):
            match = self.pattern.search(x)
            if match:
                return match.group(1)
        return self.fallback

    def fit(self, X, y=None):
        return self
    
    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.requires_fit = False
        return tags

    def transform(self, X: DataFrame) -> DataFrame:
        if ("Name" in X.columns) and self.extract:
            X_out = X.drop("Name", axis=1)
            extracted = X["Name"].map(self._extract_one)
            if self.to_replace:
                extracted = extracted.replace(self.to_replace)
            if self.valid:
                extracted.loc[~extracted.isin(self.valid)] = self.fallback
            X_out["Title"] = extracted
        else:
            X_out = X.drop("Name", axis=1, errors="ignore")
        return X_out
    
# Extract decks from cabins
class DeckExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, extract=True, 
                 valid: list[str] | None=["A", "B", "C", "D", "E", "F", "G"], 
                 to_replace: dict[str, str] | None=None, 
                 fallback="U"):
        self.extract = extract
        self.valid = valid
        self.to_replace = to_replace
        self.fallback = fallback
        self.pattern = re.compile(r"\b([A-Z])[0-9]*?\b")

    def _extract_one(self, x) -> str:
        if isinstance(x, str):
            m = self.pattern.search(x)
            if m:
                return m.group(1)
        return self.fallback

    def fit(self, X, y=None):
        return self
    
    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.requires_fit = False
        return tags

    def transform(self, X: DataFrame) -> DataFrame:
        if ("Cabin" in X.columns) and self.extract:
            X_out = X.drop("Cabin", axis=1)
            extracted = X["Cabin"].map(self._extract_one)
            if self.to_replace:
                extracted = extracted.replace(self.to_replace)
            if self.valid:
                extracted.loc[~extracted.isin(self.valid)] = self.fallback
            X_out["Deck"] = extracted
        else:
            X_out = X.drop("Cabin", axis=1, errors="ignore")
        return X_out
    
# Create new categorical feature from Sex, Pclass, Age
class SexPclassAgeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, extract=True, fallback="Other"):
        self.extract = extract
        self.fallback = fallback

    def fit(self, X, y=None):
        return self
    
    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.requires_fit = False
        return tags
    
    def _sex_pclass_age_feature(self, x):
        # x is a row
        sex = x["Sex"]
        pclass = x["Pclass"]
        age = x["Age"]
        x["SexPclassAge"] = self.fallback
        if age and sex and pclass:
            if sex == "male" and pclass == 3:
                if age <= 5:
                    x["SexPclassAge"] = f"Male, P3, Age<=5"
                elif age <= 15:
                    x["SexPclassAge"] = f"Male, P3, 5<Age<=15"
                else:
                    x["SexPclassAge"] = f"Male, P3, Age>15"
        return x

    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        if self.extract and ("Sex" in X.columns) and ("Pclass" in X.columns) and ("Age" in X.columns):
            X_out = X_out.apply(self._sex_pclass_age_feature, axis=1)
        return X_out

# Age imputation
class AgeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, model=None, 
                 feature_names={
                     "numeric": {"FamilySize", "SibSp", "Pclass", "FareTransformed"}, 
                     "ordinal": {"Sex"}, 
                     "onehot": {"Title"}}, 
                     add_indicator=False, 
                     target_name="Age"):
        
        self.feature_names = feature_names
        self.target_name = target_name
        self.model = model
        self.add_indicator = add_indicator
    
    def fit(self, X: DataFrame, y=None):
        if not(self.model == None):
            X = X.dropna(subset=[self.target_name]) # drop missing rows
            columns = set(X.columns)
            numeric = list(columns & self.feature_names["numeric"])
            ordinal = list(columns & self.feature_names["ordinal"])
            ordinal_transformations = {"Deck": get_default_encoding("Deck")}
            onehot = list(columns & self.feature_names["onehot"])
            onehot_transformations = {"Sex": get_default_encoding("Sex"), "Title": get_default_encoding("Title")}
            col_tf = build_column_transformer(numeric=numeric, onehot=onehot, onehot_transformations=onehot_transformations, ordinal=ordinal, ordinal_transformations=ordinal_transformations)
            self.pipeline_ = Pipeline([
                ("col_tf", col_tf),
                ("model", self.model),
            ])
            self.pipeline_.fit(X.drop(columns=[self.target_name], errors="ignore"), X[self.target_name])
            self.feature_names_in_ = numeric.copy()
            self.feature_names_in_.extend(ordinal)
            self.feature_names_in_.extend(onehot)
        self.is_fitted_ = True
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        check_is_fitted(self)
        X_out = X.copy()
        if (not self.add_indicator) and (self.model == None):
            return X_out
        
        missing_mask = X_out[self.target_name].isna()
        if self.add_indicator:
            X_out[self.target_name + "_Missing"] = missing_mask

        if not(self.model == None):
            if missing_mask.any():
                y_pred = self.pipeline_.predict(X_out.loc[missing_mask, self.feature_names_in_])
                X_out[self.target_name] = X_out[self.target_name].fillna(pd.Series(y_pred, index=missing_mask.loc[missing_mask].index))

        return X_out

    def get_feature_names_out(self):
        return self.feature_names_in_

# Pre-age imputation encoder
class ImputationEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        self.feature_names_in = None
    
    def fit(self, X: DataFrame, y=None):
        self.feature_names_in_ = X.select_dtypes(include=["object"]).columns
        self.encoder.fit(X.select_dtypes(include=["object"]))
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        X_tr = self.encoder.transform(X.select_dtypes(include=["object"]))
        X_out = pd.concat((X_out, pd.DataFrame(X_tr, columns=self.get_feature_names_out(), index=X_out.index)), axis=1)
        return X_out
    
    def get_feature_names_out(self):
        return [f"{name}_Ord" for name in self.feature_names_in_]


class FareImputer(BaseEstimator, TransformerMixin):
    def fit(self, X: DataFrame, y=None):
        self.mapper_ = X.groupby("Pclass")["Fare"].median().to_dict()
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        mask = X_out["Fare"].isna()
        X_out.loc[mask, "Fare"] = X_out.loc[mask, "Pclass"].map(self.mapper_)
        return X_out