What are all the components of a learning algorithm? Data, model, hyperparameters? Objective function, optimization

Bias-variance analysis, sources of bias

Go over CS229 notes on validation/cross-validation

data leakage, target leakage - I bet if a feature has 100% correlation with target, this is target leakage. https://www.kaggle.com/code/alexisbcook/data-leakage

EDA - different correlations

What is stale data? Or stale output?

What are all the infrastructure components?

Which models support statistical tests for confidence?

If I want to use ANNs for tabular data, what's a good way to construct them? Deep? How many neurons per layer?

Transforming skewed distributions by taking log

Study sklearn documentation, especially model APIs to at least understand the options that are available

Feature importance - model-specific (trees and impurity-based) and model-agnostic (permutation importance, SHAP, LIME)

Curse of dimensionality/number of features to number of samples
* Each feature is like a random variable - you want many samples per feature so you can see the underlying pattern and reduce noise

when I draw plots in a Python script, how are the plots rendered? Interactive vs. non-interactive, backend

Hands-on ML
* Chapter 1 exercises
* Appendix B

# Drill

* What is generalization error?
* What is the point of having train, validation, and test splits? What are the pitfalls of not using these splits correctly?
* What are holdout validation, cross validation, and leave-one-out validation? When do we use them/what are the advantages and disadvantages of each strategy?