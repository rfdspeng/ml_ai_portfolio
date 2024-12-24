As MLE, every day you'll work on
* Finding the best features / best model (experimentation)
* Incorporating the new data that is coming in
* Deploying the model
* Monitoring the performance of the model (receive notification if model performance starts to degrade)
* Deploy new model

Data can drift over time, e.g. the distribution of any given feature.

You can also look into the interactions between features - correlation. See if this has changed.

Evaluation metric (e.g. F1-score) is changing (deteriorating) over time. This is called model drift.

Let's say you're predicting if someone will churn. The features are the same, but the model predictions are worse. In this case, perhaps the customer behavior changed. There may be an opportunity to look for hidden information and features that could improve model performance. The model may not have the information it needs.

You can do things from scratch. 

# <u>nannyML</u>

Quantify drift. Statistical testing - read about these. There are different tests for continuous variables and categorical variables. Hypothesis testing.

Apparently you need to figure out if a variable is categorical or continuous, and there is a heuristic for this. (At least for the given example. As an MLE, you should know which types your variables are.)

```python
drift_calculator = nml.UnivariateDriftCalculator(column_names=[column_name], continuous_methods=continuous_methods, categorical_methods=categorical_methods)
drift_calculator.fit(reference_data=existing[[column_name]])
drift_result = drift_calculator.calculate(data=current[[column_name]])
drift_figure = drift_results.plot(kind="drift")
```