import re
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

# Extract family size and drop unneeded columns
class FamilySizeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, to_drop: list[str] | None=None):
        self.to_drop = set(to_drop) if to_drop else None
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        if ("SibSp" in X_out.columns) and ("Parch" in X_out.columns):
            X_out["FamilySize"] = X_out["SibSp"] + X_out["Parch"]
        if self.to_drop:
            X_out = X_out[list(set(X_out.columns) - self.to_drop)]
        return X_out

# Extract titles from names
class TitleExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, extract_titles=True, to_replace=None, valid_titles=None, fallback="Unknown"):
        self.extract_titles = extract_titles
        self.to_replace = to_replace
        self.valid_titles = valid_titles
        self.fallback = fallback
        self.pattern = re.compile(r"\b([a-zA-Z]+?)\.")

    def _extract_one(self, name) -> str:
        if isinstance(name, str):
            match = self.pattern.search(name)
            if match:
                return match.group(1)
        return self.fallback

    def fit(self, X, y=None):
        return self

    def transform(self, X: DataFrame) -> DataFrame:
        X_clean = X.drop("Name", axis=1)
        if self.extract_titles:
            titles = X["Name"].map(self._extract_one)
            if self.to_replace:
                titles = titles.replace(self.to_replace)
            if self.valid_titles:
                titles.loc[~titles.isin(self.valid_titles)] = self.fallback
                X_clean["Title"] = titles
        return X_clean

# Age imputation
class AgeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, model, feature_names: list[str] | None=None, target_name="Age"):
        self.feature_names = feature_names
        self.target_name = target_name
        self.model = model
        if self.feature_names:
            self.feature_names_in_ = self.feature_names
    
    def fit(self, X: DataFrame, y=None):
        X_train = X.dropna(subset=[self.target_name])
        if not self.feature_names:
            self.feature_names_in_ = X_train.select_dtypes(exclude=["object"]).columns.tolist()
            self.feature_names_in_.remove(self.target_name)
            # self.feature_names_in_.remove("Survived")
        
        self.model.fit(X_train[self.feature_names_in_], X_train[self.target_name])
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        missing_mask = X[self.target_name].isna()
        if missing_mask.any():
            y_pred = self.model.predict(X.loc[missing_mask, self.feature_names_in_])
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