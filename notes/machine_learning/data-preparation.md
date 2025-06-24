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
* Missing indicator: Add a boolean feature that indicates if the original value is missing. This is used in conjunction with one of the other imputation methods.
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

You get `fit_transform` for free by adding `TransformerMixin` as a base class.

If you add `BaseEstimator` as a base class and avoid `*args` and `**kwargs` in your constructor, you also get `get_params()` and `set_params()`, which will be useful for automatic hyperparameter tuning.

```python
from sklearn.base import BaseEstimator, TransformerMixin

class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, hyperparameter=default_value):
        self.hyperparameter = hyperparameter
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # transformation logic
        return X_transformed
```

Use hyperparameters to toggle off/on data preparation steps you're not 100% sure on.

# Transformation pipelines in sklearn

```python
pipeline = Pipeline([
    ("estimator1_name", estimator1_instance),
    ("estimator2_name", estimator2_instance),
    ...,
    ("estimatorLast_name", estimatorLast_instance),
    ])

transformed_dataset = pipeline.fit_transform(dataset)
```

* Except for estimatorLast, all estimators must be transformers (they must have `fit_transform()` method)
* `pipeline.fit()` calls `fit_transform` sequentially on all transformers until the final estimator, for which it calls `fit`
* Pipeline exposes the same methods as the final estimator, so you can call `pipeline.fit_transform()` if the final estimator is a transformer

Names must be unique and cannot contain double underscores (useful for hyperparameter tuning).

## ColumnTransformer

To handle both categorical and numerical attributes in one pipeline, use `ColumnTransformer` with DataFrame.

```python
pipeline = ColumnTransformer([
    ("numerical", numerical_pipeline, numerical_attribute_names),
    ("categorical", categorical_pipeline, categorical_attribute_names),
])

transformed_dataset = pipeline.fit_transform(dataset)
```

The categorical pipeline could be a simple OneHotEncoder, for example.

If the pipeline outputs are a mix of sparse and dense, ColumnTransformer estimates the density of the final matrix (ratio of nonzero cells) and returns a sparse matrix if density is lower than the threshold (default `sparse_threshold=0.3`).

* Instead of specifying a pipeline instance, you can pass string "drop" or "passthrough" to drop or leave the columns unaltered.
* `remainder` option: default option for unspecified columns