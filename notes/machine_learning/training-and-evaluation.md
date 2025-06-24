At this point, you've
* Acquired the data, explored it, performed feature engineering
* Split your data into train and test
* Written transformation pipelines (e.g. missing values, encoding, scaling) to automatically prepare your data for training the ML algorithm

# Evaluate different model types on the training set

**Important notes:**
* The goal of this step is to shortlist a few model types before tuning the hyperparameters
* You should save every model you experiment with so you can easily come back to any model. Save the hyperparameters, the trained parameters (serialize your model), cross-validation scores, and predictions.

Serialization:
* Python's built-in `pickle` module
* `joblib` - good for Python objects with large NumPy arrays
* TF/Keras/PyTorch have their own framework-specific serialization
* ONNX enables interoperability b/w different frameworks

Try a few different models with the default options.
* Tabular data, supervised learning
    * Linear or logistic regression, decision tree, random forest, gradient-boosted tree, SVM with different kernels

There is (hopefully) a pattern in the data that will allow you to make predictions. You need to pick the right model to capture that pattern - that relationship between input features and output labels.

The data will be noisy. It may also have errors and outliers that don't reflect the pattern. These may confuse your model. Your model may capture noise/errors/outliers instead of the true pattern.

Generally, as your dataset grows in size, the "signal" or pattern grows stronger and noise decreases. Central limit theorem, the error in each sample is a zero-mean random variable. (Do the math here).

In both overfitting and underfitting, your model is not capturing the pattern/relationship. When your model overfits, it's capturing noise (in addition to pattern). When your model underfits, it's unable to capture any pattern at all, noise or true relationship.

If your model is overfitting to the training data, you can
* Gather more training data (which reduces noise)
* Simplify the model: pick a simpler model or constrain the model (regularization) so it's unable to capture the noise
* Clean the training data: remove or clean the samples that don't represent the true relationship
    * Get rid of errors and/or outliers
    * Remove uninformative features (feature engineering)
    * Combine raw features into more useful features (feature engineering)

If your model is underfitting, you can
* Increase the complexity of the model: select a more powerful model, with more parameters, or reduce the model constraints (e.g. reduce regularization)
* Combine raw features into more useful features (feature engineering) - if this works, I think that means that the raw features don't represent the true relationship on their own. The features themselves don't carry the information that allows us to separate the classes/predict continuous value.

Curse of dimensionality - as number of features goes up, you need more samples to "see" the pattern because the data gets very sparse as number of dimensions increases.

Use some kind of validation to see if the model is overfitting, like holdout or K-fold cross-validation. With K-fold, you can calculate the average and standard deviation of the target performance metric.

# Hyperparameter tuning

When you have no idea what a hyperparameter should be, a simple approach is to try consecutive powers of 10, e.g. 0.01, 0.1, 1, 10, 100, etc.

**Remember: hyperparameters in any estimator instance in sklearn can be tuned, including components in the data preparation/transformation pipeline.** GridSearchCV with Pipeline: https://scikit-learn.org/stable/auto_examples/compose/plot_compare_reduction.html#sphx-glr-auto-examples-compose-plot-compare-reduction-py

## Grid search

For each hyperparameter, specify the values you want to sweep. Each possible combination of hyperparameters is searched.

`sklearn.model_selection.GridSearchCV` implements grid search with cross validation.
* Important constructor parameters: `param_grid`, `cv`, `scoring`, `return_train_score`
* Important attributes: `best_params_`, `best_estimator_`, `cv_results_`

## Randomized search

Grid search is also known as exhaustive search and is impractical for huge numbers of hyperparameter combinations.

In randomized search, you specify the number of iterations. In each iteration, it randomly selects values for each hyperparameter. Benefits:
* You can sweep many different values for each hyperparameter instead of just a few like in grid search
* You have more control over the computing budget since it's determined only by number of iterations

## Ensemble methods

Try combining different models that perform the best.

## Analyze the best models and their errors

You will often gain good insights on the problem by inspecting the best models. For example, tree-based models indicate the relative importance of each attribute for making accurate predictions.

Inspect the specific errors in the predictions, try to understand what causes them, and try to fix the problem: add extra features, remove uninformative features, clean up outliers, etc.

# Evaluate on the test set

