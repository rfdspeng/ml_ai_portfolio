# References

* Hands-On Machine Learning
* https://scikit-learn.org/stable/model_selection.html
* Stanford CS229 notes
* https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html
* The Elements of Statistical Learning
* https://www.cs.cmu.edu/~psarkar/sds383c_16/lecture9_scribe.pdf

# Model selection

At this point, you're ready for model selection. You've
* Acquired the data, explored it, performed feature engineering
* Split your data into train and test (if necessary)
* Written transformation pipelines (e.g. missing values, encoding, scaling) to automatically prepare your data for training the ML algorithm

The goal of model selection is to fine-tune the learning algorithm - the model and the hyperparameters - so the model learns from the training data and generalizes to unseen data. This means finding the optimal balance between bias and variance.

## Overfitting and underfitting, bias-variance tradeoff

The goal of learning algorithms, both supervised and unsupervised, is to capture the "true" patterns in the data. In the case of supervised learning, we want to capture the relationship between input features and output labels.

The learning algorithm has two sources of information:
1. The model assumptions (this information comes from you, the data scientist). This is also known as inductive bias.
The stronger the assumptions, the higher the inductive bias of the model.
2. The training data

If your model is too simple, it is unable to capture the pattern, and it will have poor performance on both training and validation data. Your model has _high bias_ and is _underfitting_.

Data is noisy. It has errors and outliers that are not part of the pattern. If your model is too complex (or too flexible), it will capture both the pattern and the noise in your training data, and it will not generalize well to unseen data. It will have good performance on training data and poor performance on validation data. Your model has _high variance_ and is _overfitting_.

Both overfitting and underfitting means that your model is not capturing the true patterns in the data.

With good sampling, as your dataset grows in size, the "signal" or pattern grows stronger and the effect of noise is reduced. 

If your model is overfitting to the training data, you can
* Gather more training data (which reduces noise)
* Simplify the model: pick a simpler model or constrain the model (regularization) so it's unable to capture the noise
* Clean the training data: remove or clean the samples that don't represent the true relationship
    * Get rid of errors and/or outliers
    * Remove uninformative features (feature selection)

If your model is underfitting, you can
* Increase the complexity of the model: select a more powerful model, with more parameters, or reduce the model constraints (e.g. reduce regularization)
* Combine raw features into more useful features (feature extraction): when the raw features are not good predictors

## Cross-validation

To evaluate if the learning algorithm is overfitting or underfitting, we typically use cross-validation. 

The simplest is _holdout validation_: split your training data further into one training set and one validation set. Train on the training set and estimate _generalization error_ (aka out-of-sample error) on the validation set.

If you can afford training multiple times, _K-fold cross-validation_ is a better strategy.
* You train and validate on the entire training set (more efficient use of data)
* The estimate of generalization error is the mean error across _K_ folds, which is less susceptible to random variation than holdout validation, where you only get one estimate of generalization error
* Calculate the standard error of the estimate
    * You have _K_ samples
    * The mean generalization error is an estimate of the true generalization error
    * The standard error for _K_ samples is given by $\sigma/\sqrt(K)$, where $\sigma$ is the standard deviation of the _K_ samples
    * Keep in mind that since the _K_ samples are not entirely independent (the folds overlap), the standard error underestimates the uncertainty of the estimate
    * As _K_ increases, standard deviation will tend to increase since validation size decreases

## Hyperparameter tuning

Remember: a hyperparameter is a parameter of the learning algorithm, not of the model. The model you choose is a hyperparameter, e.g. linear regression. The model parameters are b, a1, a2, etc. Hyperparameters are selected prior to training.

We can use cross-validation to evaluate generalization error. To optimize the hyperparameters for generalization error (finding the best balance of bias and variance), we use hyperparameter tuning: for each cross-validation, we may change
* The model
* The model hyperparameters
* The learning algorithm hyperparameters
* The data preparation pipeline

**Remember: hyperparameters in any estimator instance in sklearn can be tuned, including components in the data preparation/transformation pipeline.**

Recommendations from Hands-On Machine Learning:
* Shortlist a few models (using default options) before tuning the hyperparameters
    * Supervised learning with structured data: linear or logistic regression, decision tree, random forest, gradient-boosted tree, SVM with different kernels
    * Unsupervised learning with structured data:
    * Supervised learning with time-series data
    * ?
* Save every model you experiment with so you can easily come back to any model. Save the hyperparameters, the trained parameters (serialize your model), cross-validation scores, and predictions.
* When you have no idea what a hyperparameter should be, a simple approach is to try consecutive powers of 10, e.g. 0.01, 0.1, 1, 10, 100, etc.

Serialization options:
* Python's built-in `pickle` module
* `joblib` - good for Python objects with large NumPy arrays
* TF/Keras/PyTorch have their own framework-specific serialization
* ONNX enables interoperability b/w different frameworks

Simple strategies for hyperparameter tuning:
* _Grid search_: For each hyperparameter, specify the values you want to sweep. Each possible combination of hyperparameters is searched.
* _Randomized search_
    * Grid search is also known as exhaustive search and is impractical for huge numbers of hyperparameter combinations
    * In randomized search, you specify the number of iterations. In each iteration, it randomly selects values for each hyperparameter. Benefits:
        * You can sweep many different values for each hyperparameter instead of just a few like in grid search
        * You have more control over the computing budget since it's determined only by number of iterations

### One standard error rule

Any time we use the same data for optimizing the model and evaluating the model performance, there is a possibility of overfitting.

One popular strategy for preventing overfitting the hyperparameters is the one standard error rule. Rather than picking the model with the best cross-validation performance, we pick the simplest model that has reasonably similar performance. Specifically,
* For the model with the best mean generalization error, calculate the standard error
* Pick the simplest model with performance within one standard error of the best model

### Nested cross-validation

Nested CV estimates the generalization error of the underlying model and its hyperparameter search.

Basically, you split twice.
* In the outer loop, you split the data into _K_ outer folds. Let's say _K_ is 5. In the first outer iteration, 1 fold is your test fold and the remaining 4 are your training set.
* You further split the training set into _L_ inner folds and tune hyperparameters on the training set, as normal. Choose the best hyperparameters, retrain the model on the entire training set, and then calculate generalization error on the outer test fold. Repeat this for all _K_ folds to get _K_ estimates of generalization error.

This is similar to having a test set, except of course the _K_ folds are not totally independent.

You can implement nested CV in `sklearn` by passing a grid or randomized search object into a cross validation function. However, note that this cannot be directly used to find the best hyperparameters - each outer fold may have chosen different hyperparameters, and from what I've seen, the grid search object doesn't save any results anyway. 

In other words,
* Use regular CV for hyperparameter tuning
* Use nested CV to get a less biased estimate of how well the model generalizes

## What about bootstrapping?



## Ensemble methods

Try combining different models that perform the best.

## Analyze the best models and their errors

You will often gain good insights on the problem by inspecting the best models. For example, tree-based models indicate the relative importance of each attribute for making accurate predictions.

Inspect the specific errors in the predictions, try to understand what causes them, and try to fix the problem: add extra features, remove uninformative features, clean up outliers, etc.

Let's take Titanic as an example. You can create subsets of your validation dataset that represent different groups of people (lower class, children, women, etc.) and compare model accuracy across these different groups.

## Tuning the decision threshold for class prediction

Classification is best divided into two parts:
* The statistical problem of learning a model to predict class probabilities
* The decision problem to take concrete action based on those probability predictions

The difference, for example, is between these two questions:
* What is the chance that it will rain tomorrow?
* Should I take an umbrella tomorrow?

* `predict_proba`: default threshold = 0.5. Returns conditional probability estimates - $P(y|X)$ - for each class.
* `decision_function`: default threshold = 0. Returns decision scores for each class. Represents the distance of the sample from the decision boundary. Only available for some classifiers, like `LogisticRegression` - in logistic regression, the decision function is equal to the dot product of the input vector with the parameter vector.

The default threshold of 0.5 often doesn't make sense. For example, if there is a 45% of rain. Cost-sensitive learning. Etc.

`TunedThresholdClassifierCV`
* Tunes the decision threshold using internal cv. The optimum threshold is chosen to maximize a metric given via `scoring` (balanced accuracy is the default metric).
* By default, uses 5-fold stratified cv; controllable via `cv`. You can bypass cv with `cv="prefit"` and provide a fitted classifier; then the decision threshold is tuned on the data provided to `fit`. 

# Estimate generalization error on the test set

Any time we use the same data for optimizing the model and evaluating the model performance, there is a possibility of overfitting.

For example, we learned the model parameters from the training data. The parameters have been optimized to fit the training data. Given new data, it's unlikely that the model will perform as well.

We tuned the model hyperparameters based on the validation data. The hyperparameters have been optimized for the validation data. Given new data, it's unlikely that the model will perform as well.

That's the point of having a test set - to get a true (unbiased) estimate of your generalization error. (In academia, it is absolutely necessary to have a test set for estimating generalization error, but in industry/production, you may choose not to have a test set.) If test performance is worse than validation, YOU MUST NOT TWEAK THE LEARNING ALGORITHM. That defeats the point of the test set, which is just to estimate generalization error.

Let's say your generalization error is 0.1% better than a previous model. How confident are we that this model is better?

For that, we can calculate a confidence interval (t-distribution for regression, Z-distribution for classification - fill this in). Additional resources:
* MHIST paper – they used 10 random seeds.
* https://sebastianraschka.com/blog/2022/confidence-intervals-for-ml.html

# Data leakage

If we select predictors for the labels based on the entire training set before splitting into _K_ folds for cross-validation, this is one example of target leakage (from _Elements_).

# Project pre-launch

* Present solution
    * What did you learn?
    * What worked and what didn't work?
    * What are your assumptions?
    * What are the system limitations?
* Document everything
* Create presentations with clear visualization and easy-to-remember statements, like "the median income is the number one predictor of housing prices"