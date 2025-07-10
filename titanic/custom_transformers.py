import re
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

# Extract family size and drop unneeded columns
class FamilySizeExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, max_famsize: int | None=None, to_drop: list[str] | None=None):
        self.max_famsize = max_famsize
        self.to_drop = set(to_drop) if to_drop else None
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.copy()
        if ("SibSp" in X_out.columns) and ("Parch" in X_out.columns):
            X_out["FamilySize"] = (X_out["SibSp"] + X_out["Parch"]).clip(upper=self.max_famsize)
        if self.to_drop:
            X_out = X_out[list(set(X_out.columns) - self.to_drop)]
        return X_out

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

    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.drop("Name", axis=1)
        if self.extract:
            extracted = X["Name"].map(self._extract_one)
            if self.to_replace:
                extracted = extracted.replace(self.to_replace)
            if self.valid:
                extracted.loc[~extracted.isin(self.valid)] = self.fallback
            X_out["Title"] = extracted
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

    def transform(self, X: DataFrame) -> DataFrame:
        X_out = X.drop("Cabin", axis=1)
        if self.extract:
            extracted = X["Cabin"].map(self._extract_one)
            if self.to_replace:
                extracted = extracted.replace(self.to_replace)
            if self.valid:
                extracted.loc[~extracted.isin(self.valid)] = self.fallback
            X_out["Deck"] = extracted
        return X_out

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