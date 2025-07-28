Hands-on Machine Learning: sklearn's API is remarkably well designed.
* All objects share a consistent and simple interface
* _Estimators_: Any object that can estimate some parameters based on a dataset is called an estimator. Estimation is performed with `fit(dataset(s))` method. Any parameter needed for estimation is a hyperparameter and must be set as an instance variable (generally via a constructor parameter). `fit` returns `self`.
* _Transformers_: Some estimators can transform a dataset. Transformation is performed with `transform(dataset)` method. Relies on the learned parameters. `fit_transform()` is equivalent to calling `fit()` followed by `transform()` but can be much faster. `transform` returns the transformed dataset.
* _Predictors_: Some estimators, given a dataset, can make predictions. Predictions are made with `predict(dataset)` method. `score()` measures quality of predictions.
* All estimator hyperparameters are accessible via public instance variables (e.g. `imputer.strategy`) and all learned parameters are accessible via public instance variables with an underscore suffix (e.g. `imputer.statistics_`).
* No new data classes: Datasets are NumPy arrays or SciPy sparse matrices. Hyperparameters are regular Python strings or numbers.
* Modular using `Pipeline` estimator
* Sensible default values