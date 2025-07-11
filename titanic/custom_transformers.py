import re
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.utils.validation import check_is_fitted

class DynamicDataPrepPipeline(BaseEstimator, TransformerMixin):
    def __init__(self, extract_fam=False, fam_kwargs={}, 
                 extract_title=False, title_kwargs={}, 
                 extract_deck=False, deck_kwargs={},
                 extract_sexpclassage=False, sexpclassage_kwargs={},
                 numeric_columns={"Age", "Pclass", "Fare"},
                 onehot_columns=set(),
                 ordinal_columns={"Sex"}):
        self.extract_fam = extract_fam
        self.fam_kwargs = fam_kwargs
        self.extract_title = extract_title
        self.title_kwargs = title_kwargs
        self.extract_deck = extract_deck
        self.deck_kwargs = deck_kwargs
        self.extract_sexpclassage = extract_sexpclassage
        self.sexpclassage_kwargs = sexpclassage_kwargs
        self.numeric_columns = numeric_columns
        self.onehot_columns = onehot_columns
        self.ordinal_columns = ordinal_columns
    
    def fit(self, X: DataFrame, y=None):
        # Instantiate extractors
        fam = FamilySizeExtractor(**self.fam_kwargs)
        fam.extract = self.extract_fam

        title = TitleExtractor(**self.title_kwargs)
        title.extract = self.extract_title

        deck = DeckExtractor(**self.deck_kwargs)
        deck.extract = self.extract_deck

        sexpclassage = SexPclassAgeExtractor(**self.sexpclassage_kwargs)
        sexpclassage.extract = self.extract_sexpclassage

        # Build extractor pipeline
        feature_extractor = Pipeline([
            ("fam", fam),
            ("title", title),
            ("deck", deck),
            ("sexpclassage", sexpclassage)
        ])

        # Run extractors to find out what columns they output
        # X_extracted = feature_extractor.fit_transform(X)

        # Dynamically choose columns
        numeric = list(set(X.select_dtypes(exclude=["object", "category"]).columns) & self.numeric_columns)
        ordinal = list(set(X.select_dtypes(include=["object", "category"]).columns) & self.ordinal_columns)
        onehot = list(set(X.select_dtypes(include=["object", "category"]).columns) & self.onehot_columns)

        self.feature_names_in_ = numeric.copy()
        self.feature_names_in_.extend(ordinal)
        self.feature_names_in_.extend(onehot)

        # if 'FamilySize' in X_extracted.columns:
        if self.extract_fam:
            numeric.append('FamilySize')

        # if 'Title' in X_extracted.columns:
        if self.extract_title:
            onehot.append('Title')

        # if 'Deck' in X_extracted.columns:
        if self.extract_deck:
            ordinal.append('Deck')
        
        # if "SexPclassAge" in X_extracted.columns:
        if self.extract_sexpclassage:
            onehot.append('SexPclassAge')
        
        self.feature_names_out_ = numeric.copy()
        self.feature_names_out_.extend(ordinal)
        self.feature_names_out_.extend(onehot)

        # Build column transformer
        col_tf = ColumnTransformer(
            ([('num', "passthrough", numeric)] if numeric else []) + 
            ([("onehot", OneHotEncoder(handle_unknown="ignore"), onehot)] if onehot else []) +
            ([("ord_sex", OrdinalEncoder(
                categories=[["male", "female"]], 
                handle_unknown="error",
                ), 
            ["Sex"])] if "Sex" in ordinal else []) + 
            ([("ord_deck", OrdinalEncoder(
                categories=[["A", "B", "C", "D", "E", "F", "G", "U"]],
                handle_unknown="error", # unknowns are handled in preprocessing
                # handle_unknown="use_encoded_value",
                # unknown_value=7,
                # encoded_missing_value=7,
                ), 
            ["Deck"])] if "Deck" in ordinal else [])
            , remainder="drop")

        # Final full pipeline
        self.pipeline_ = Pipeline([
            ("extractor", feature_extractor),
            ("col_tf", col_tf)
        ])

        self.pipeline_.fit(X, y)
        # self._is_fitted = True
        return self

    def transform(self, X):
        # check_is_fitted(self)
        return self.pipeline_.transform(X)
    
    def get_feature_names_out(self):
        return self.pipeline_.named_steps["col_tf"].get_feature_names_out()

    # def __sklearn_is_fitted__(self):
    #     """
    #     Check fitted status and return a Boolean value.
    #     """
    #     return hasattr(self, "_is_fitted") and self._is_fitted

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