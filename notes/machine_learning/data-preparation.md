# References

* Hands-On ML
* https://scikit-learn.org/stable/developers/develop.html#apis-of-scikit-learn-objects
* https://scikit-learn.org/stable/modules/grid_search.html
* https://scikit-learn.org/stable/modules/compose.html#pipeline

# Handling missing values

When values are missing, you can either omit the associated samples/attributes or you can impute (infer) the missing values.

You can consider omission when
* Only a small number of values are missing (in percentage/proportion)
* Missing values are missing completely at random (MCAR) so that removing them won't change the feature distribution. If you identify patterns of missing data, then this is information you should not remove.
* A sample (row) is missing most of its attributes or critical attributes
* An attribute (column) is missing most of its values

There are a few different techniques for imputing missing values.
* Simple imputation: Replace missing values with a summary statistic or a constant. Be careful of introducing bias into your data.
    * For numerical, this is usually mean, median, or mode, depending on your distribution.
    * For categorical, this is usually mode.
* Group-wise imputation: Similar to simple imputation, but you first organize the data into different (and logical) groups. Groups should be large enough to compute stable summary statistics.
* Missing indicator: Add a boolean feature that indicates if the original value is missing. This can be used in conjunction with one of the other imputation methods or on its own.
* Predictive imputation: Train a supervised model to fill in missing values based on other features. Because of its complexity, this is not a practical method for large datasets.
    * If you want to impute during inference, you CANNOT use the label to train the imputer
    * If you only need to impute training data, you CAN use the label to train the imputer
* KNN imputation: Uses KNN with a euclidean distance metric that supports missing values. Finds the nearest neighbors and imputes missing values based on an average of the nearest neighbors.
* Interpolation (for numerical data that is a function of time or location)

Some ML algorithms inherently handle missing values (like trees, I think).

MCAR, MAR, MNAR

Check out sklearn library for imputation: https://scikit-learn.org/stable/modules/impute.html

# Encoding categorical attributes

Categorical attributes, if not already represented as numbers, need to be converted to numbers before being fed to the learning algorithm.

**Ordinal encoding:**
* Convert categories to whole numbers, 0 to n_categories-1
* You should use this encoding for attributes that have order, intensity, scale, etc. For example, a rating that has 4 categories: "bad", "average", "good", "excellent".

**One-hot encoding:**
* Create one binary attribute per category: if your attribute has n_categories, then it is encoded as a one-hot vector of size n_categories. 
* The new attributes are sometimes called dummy attributes
* If you have m samples, then the attribute is encoded as a sparse matrix of size m * (n_categories).
* Sparse matrix (SciPy) only stores the location of nonzero elements. You can use the matrix mostly as you would use a normal 2D array, but you can also explicitly convert it to a NumPy dense array if needed.
* If a categorical attribute has a large number of possible categories, then one-hot encoding will explode the number of input features, which may slow down training. In this case, you may want to replace it with useful numerical features instead (e.g. country code -> country population and GDP per capita) or with an embedding.


Embedding:
* Learnable, low-dimensional vector
* Representation learning: each category's representation is learned during training

# Feature scaling

With few exceptions (e.g. decision trees), ML algorithms don't perform well when input numerical attributes have very different scales. Larger features are heavily weighted during optimization.

**As with all transformations, it's important to fit scalers only to the training set, while transformations are applied to all sets.**

**Min-max scaling, aka normalization:** 
* Values are shifted and rescaled so they are clipped to the range [0, 1]
* Subtract all values by min, then divide by (max - min)

**Standardization:**
* Subtract all values by mean, then divide by standard deviation
* The resulting distribution has zero mean, unit variance
* Does not bound values to a specific range (which may be a problem for some algorithms)
* Much less affected by outliers compared to min-max scaling

# Custom transformers in sklearn

sklearn relies on duck typing (not inheritance), so all you need to do is create a class and implement 3 methods: `fit()` (returning self), `tranform()`, and `fit_transform()`.

You get `fit_transform` for free by adding `TransformerMixin` as a base class (`fit_transform` is required for pipelining this estimator).

If you add `BaseEstimator` as a base class and avoid `*args` and `**kwargs` in your constructor, you also get `get_params()` and `set_params()`, which will be useful for automatic hyperparameter tuning. Call `get_params()` to get the list of parameters that may be tuned when using search algorithms (like grid search). `set_params()` is called by the search algorithm when tuning.

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, hyperparameter=default_value):
        self.hyperparameter = hyperparameter
    
    def fit(self, X, y=None):
        # Fitting logic (if any)
        self.fitted_attribute_ = 1 # any attributes that are created during fit should be appended with an underscore
        return self
    
    def transform(self, X):
        check_is_fitted(self)
        X_out = X.copy()
        # Transformation logic
        return X_out
```

Use hyperparameters to toggle off/on data preparation steps you're not 100% sure on.

`check_is_fitted`:
* sklearn recommends calling the utility function `check_is_fitted` at the beginning of `transform` and `predict` methods. `check_is_fitted` checks for an attribute with a trailing underscore to verify that `fit` has been called.
* You may modify the behavior of `check_is_fitted` by defining a custom method `def __sklearn_is_fitted__(self):`. `check_is_fitted` will then simply return the output of this method.
* If your estimator does not require fitting, you may "signal" this via estimator Tags. See https://scikit-learn.org/stable/developers/develop.html#estimator-tags.

Other useful attributes and methods to define:
* feature_names_in_
* get_feature_names_out()

# Transformation pipelines, hyperparameter tuning

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("estimator1_name", estimator1_instance),
    ("estimator2_name", estimator2_instance),
    ...,
    ("estimatorLast_name", estimatorLast_instance),
    ],
    memory="path") # used to cache fitted transformers (default is None). Use caching when fitting the transformers is costly and you want to load state from cache instead of refitting.

transformed_dataset = pipeline.fit_transform(dataset)
```

* Except for estimatorLast, all estimators must be transformers (they must have `fit_transform()` method)
* `pipeline.fit()` calls `fit_transform` sequentially on all transformers until the final estimator, for which it calls `fit`
* Pipeline exposes the same methods as the final estimator, so you can call `pipeline.fit_transform()` if the final estimator is a transformer

Names must be unique and cannot contain double underscores because double underscores are used for hyperparameter tuning.

For example, here is the data prep pipeline I defined for the Titanic dataset:
```python
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

    # def fit
    # def transform
```

The constructor parameters modify the components in the data prep pipeline, and you can automatically experiment with different combinations of parameters using grid search. 
* The syntax for passing hyperparameters is `"<estimator>__<parameter>": [list of values to try]"`. This syntax supports nested estimators. For example, if the top-level estimator has a parameter that is an estimator, then you can tune the sub-estimator via `"<estimator_top>__<estimator_sub>__<estimator_sub_param>"`.
* Instead of passing hyperparameters, you can pass estimators, e.g. `"<estimator>": [list of estimators to try]`.
* Call `Pipeline.get_params()` to see a list of parameters that can be set via `Pipeline.set_params()`

```python
data_prep_pipe = DynamicDataPrepPipeline()
model = RandomForestClassifier(max_depth=12, random_state=0)

ml_pipe = Pipeline([
    ("data_prep", data_prep_pipe),
    ("model", model)
])

param_grid = [
    {
        "data_prep__extract_title": [False, True],
        "data_prep__extract_fam": [False, True],
        "data_prep__extract_deck": [False, True],
        "data_prep__extract_sexpclassage": [False, True],
        "model__max_depth": [200, 10, 5],
    },
]

grid = GridSearchCV(ml_pipe, param_grid=param_grid, cv=20, scoring="accuracy", return_train_score=True)
grid.fit(df.drop("Survived", axis=1), df["Survived"])
```

There are multiple ways of accessing the components in a pipeline:
* `Pipeline.named_steps` - dict-like data structure with component names as keys, e.g. `Pipeline.named_steps["estimator"]`
* `Pipeline["estimator"]`
* `Pipeline[:]` - can be sliced, e.g. `Pipeline[0]` and `Pipeline[-1]` return the first and last components

## ColumnTransformer

To handle both categorical and numerical attributes in one pipeline, use `ColumnTransformer` with DataFrame.

```python
col_transformer = ColumnTransformer([
    ("numerical", numerical_pipeline, numerical_attribute_names),
    ("categorical", categorical_pipeline, categorical_attribute_names),
])

transformed_dataset = col_transformer.fit_transform(dataset)
```

The categorical pipeline could be a simple OneHotEncoder, for example.

If the ColumnTransformer outputs are a mix of sparse and dense, ColumnTransformer estimates the density of the final matrix (ratio of nonzero cells) and returns a sparse matrix if density is lower than the threshold (default `sparse_threshold=0.3`).

* Instead of specifying a pipeline instance, you can pass string "drop" or "passthrough" to drop or leave the columns unaltered.
* `remainder` option: default option for unspecified columns

Access components via `ColumnTransformer["estimator_name"]` or `ColumnTransformer.named_transformers_["estimator_name"]`.

Call `ColumnTransformer.get_params()` to see the list of parameters that can be set via `ColumnTransformer.set_params()`.