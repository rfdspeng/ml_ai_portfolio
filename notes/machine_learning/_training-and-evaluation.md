# References

* Hands-On Machine Learning
* https://scikit-learn.org/stable/model_selection.html

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

The simplest is _holdout validation_: split your training data further into one training set and one validation set. Train on the training set and measure _generalization error_ (aka out-of-sample error) on the validation set.

If you can afford training multiple times, _K-fold cross-validation_ is a better strategy.
* You train and validate on the entire training set
* You train and validate _K_ times so you can have more confidence in your generalization error (less susceptible to random variation than holdout validation)
* You can get an estimate of how much generalization error might vary by calculating the standard error of your _K_ generalization errors

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

### Nested cross-validation

We train the model on the training data and tune the hyperparameters on the validation data. Our learning algorithm has learned from both the training and validation data, which means that validation error will typically underestimate true generalization error.

We can get a better estimate of generalization error by using nested cross-validation.

This isn't exactly to get the best hyperparameters.

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
* `decision_function`: default threshold = 0. Returns decision scores for each class. Only available for some classifiers, like `LogisticRegression`. Represents the distance of the sample from the decision boundary - is this the raw logit/theta_T*sample?

The default threshold of 0.5 often doesn't make sense. For example, if there is a 45% of rain. Cost-sensitive learning. Etc.

`TunedThresholdClassifierCV`
* Tunes the decision threshold using internal cv. The optimum threshold is chosen to maximize a metric given via `scoring` (balanced accuracy is the default metric).
* By default, uses 5-fold stratified cv; controllable via `cv`. You can bypass cv with `cv="prefit"` and provide a fitted classifier; then the decision threshold is tuned on the data provided to `fit`. 

# Evaluate on the test set

Run your model on the test set and calculate the generalization error (MSE, accuracy, whatever). This is an estimate of the real generalization error (sample vs. population). Let's say this generalization error is 0.1% better than a previous model. How confident are we that this model is better?

For that, we can calculate a confidence interval (fill this in).
* MHIST paper – they used 10 random seeds.
* https://sebastianraschka.com/blog/2022/confidence-intervals-for-ml.html

If you did a lot of hyperparameter tuning, performance on the test set will usually be slightly worse than performance in cross-validation because your learning algorithm will be fine-tuned to perform well on the validation data and will likely not generalize as well to unseen data. When this happens, you must resist the temptation to tweak the learning algorithm to improve performance on the test set.

# Data leakage

# Project pre-launch

* Present solution
    * What did you learn?
    * What worked and what didn't work?
    * What are your assumptions?
    * What are the system limitations?
* Document everything
* Create presentations with clear visualization and easy-to-remember statements, like "the median income is the number one predictor of housing prices"