# References

* Hands-On Machine Learning

# Evaluate different model types on the training set

At this point, you've
* Acquired the data, explored it, performed feature engineering
* Split your data into train and test
* Written transformation pipelines (e.g. missing values, encoding, scaling) to automatically prepare your data for training the ML algorithm

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

## Overfitting and underfitting, bias-variance tradeoff

The goal of learning algorithms, both supervised and unsupervised, is to capture the "true" patterns in the data. In the case of supervised learning, we want to capture the relationship between input features and output labels.

The learning algorithm has two sources of information:
* The model assumptions (this information comes from you, the data scientist). This is also known as inductive bias.
The stronger the assumptions, the higher the inductive bias of the model.
* The training data

If your model is too simple, it is unable to capture the pattern, and it will have poor performance on both training and test data.

Data is noisy. It has errors and outliers that are not part of the pattern. If your model is too complex (or too flexible), it will capture both the pattern and the noise in your training data, and it will not generalize well to unseen data.

Both overfitting and underfitting means that your model is not capturing the true relationship (and only the true relationship).

With good sampling, as your dataset grows in size, the "signal" or pattern grows stronger and the effect of noise is reduced. 

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

Use some kind of validation to see if the model is overfitting, like holdout or K-fold cross-validation. With K-fold, you can calculate the average and standard deviation of the target performance metric. With K-fold, you probably want to pay attention to standard deviation - I think both mean and standard deviation are important for seeing how well your model generalizes.

Curse of dimensionality - as number of features goes up, you need more samples to "see" the pattern because the data gets very sparse as number of dimensions increases.



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

Let's take Titanic as an example. You can create subsets of your validation dataset that represent different groups of people (lower class, children, women, etc.) and compare model accuracy across these different groups.

# Evaluate on the test set

Run your model on the test set and calculate the generalization error (MSE, accuracy, whatever). This is an estimate of the real generalization error (sample vs. population). Let's say this generalization error is 0.1% better than a previous model. How confident are we that this model is better?

For that, we can calculate a confidence interval (fill this in).
* MHIST paper – they used 10 random seeds.
* https://sebastianraschka.com/blog/2022/confidence-intervals-for-ml.html

If you did a lot of hyperparameter tuning, performance on the test set will usually be slightly worse than performance in cross-validation because your learning algorithm will be fine-tuned to perform well on the validation data and will likely not generalize as well to unseen data. When this happens, you must resist the temptation to tweak the learning algorithm to improve performance on the test set.

# Project pre-launch

* Present solution
    * What did you learn?
    * What worked and what didn't work?
    * What are your assumptions?
    * What are the system limitations?
* Document everything
* Create presentations with clear visualization and easy-to-remember statements, like "the median income is the number one predictor of housing prices"