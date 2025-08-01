# Notes

* I've improved cross-validation accuracy from 79% to 83% by applying feature engineering. However, the test accuracy remains stuck at 77.5%.
    * The model is predicting that all men die - it is not able to distinguish men that survive, even on the training data. The model overestimates women surviving. I think that's why generalization is not much better than the gender model, and I think that means my model is too biased.
    * Potential causes: train-test distribution difference (like data drift), data leakage, overfitting
        * I don't think it's data leakage - I use pipelines for cross-validation
        * I don't think I'm overfitting to the validation data - I'm using cross-validation, and I see that validation performance for each fold is improving; it's not just the average across folds that's improving.
        * Train-test distributions are similar but not identical. It could be this, plus my model seems to be too biased (although increasing max_depth for the random forest only degrades cv performance).
    * Learning curves
        * Max depth = 5: too much bias
        * Max depth = 20: can learn, too much variance
        * With the tutorial's suggested features, the model cannot fit even when unconstrained. Bias is data-limited.
        * In all cases I tried, validation performance topped out at 84% - basically no improvement no matter what I tried. Adding regularization did not help; it only degraded the model's ability to fit. This suggests that there simply isn't enough training data.
        * You could try utilizing monotonic constraints but you will need to impute all missing values, plus it may not help much if at all
        * Did not try randomized search for the sake of time
    * Gradient boosting classifier doesn't improve performance
    * Decision tree classifier performance isn't that much worse - so it looks like random forest and gradient boosting tree is not providing much benefit
    * Feature engineering
        * Dropping age vs. passthrough vs. impute - dropping age hurts for very low sample size but for the full training set, it doesn't make any difference. However, if you do impute age, you should run cross-validation - some kind of check of imputation quality.
    * Next steps
        * Try reducing n_estimators to speed up training
        * Check calibration curves per subgroup
        * Do other models make different decisions?
            * Add Fare imputation - maybe a simple group-wise imputer by Pclass/AgeBin (this is only necessary for the test set)
            * Logreg, naive Bayes, GDA, SVM, KNN
            * PCA
        * Does tuning the decision threshold make sense for improving accuracy?
        * Try ensembling - before you do this, analyze the mistakes that your models are making. Ensembling models that make the same predictions may not help.
        * Data augmentation?
        * Are there any other features to play around with?
        * Different models for different subgroups?
        * Does the slight difference in train-test distribution explain why test generalization does not improve?
        * Try replicating someone else's setup - see if they just got lucky. I bet a lot of those old scores are on the 209 samples.
* Other things to look into
    * Feature selection, feature permutation for importance
    * Understand random forests and gradient boosting algorithms
        * Can you visualize the decision path?
    * Try using many different models for practice (this will require different kinds of preprocessing and feature engineering)
    * Use PCA to visualize the data points and decision boundary