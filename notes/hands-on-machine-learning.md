# Chapter 1 Fundamentals of machine learning

## What is machine learning? Why use machine learning?

[Machine Learning is the] field of study that gives computers the ability to learn without being explicitly programmed. (Arthur Samuel, 1959)

A computer program is said to learn from experience E with respect to some task T
and some performance measure P, if its performance on T, as measured by P,
improves with experience E. (Tom Mitchell, 1997)

E = training data, P = performance metric (e.g. accuracy)

Spam filter:
* Traditional method -> study the problem (analyze spam/ham emails), write rules, iterate (analyze errors) -> launch
* ML method -> study the problem, train ML algorithm using training data, iterate model/data -> launch

Benefits of ML method:
* Can automatically update for changes, e.g. spammers finding new ways to write spam to get by the filter (retraining on new data)
* Shines for problems too complex for traditional method or have no known algorithm
* Can help humans learn - inspect ML algorithms to see what they've learned, e.g. inspect the model for which words/phrases are the best predictors of spam. Sometimes this can help discover patterns not immediately apparent - this is _data mining_.

## Example applications

* Image classification, semantic segmentation -> CNNs
* Text classification, summarization, speech recognition, and anything involving sequences -> RNNs, CNNs, transformers
* Regression -> linear or polynomial regression, regression SVM, regression random forest, ANN
* Anomaly detection
* Clustering (e.g. segmenting clients based on purchases so you can design a different marketing strategy for each segment)
* Data visualization of high-dimensional datasets, often involving dimensionality reduction techniques
* Recommender systems -> train ANN on history of past purchases to get most likely next purchase
* Reinforcement learning to train agents (such as bots) to maximize rewards over time

## Types of ML systems

Broad classifications:
* Trained with human supervision? (supervised, unsupervised, semisupervised, reinforcement learning)
* Can learn incrementally on the fly? (online vs. batch learning)
* Compare new data points to known data points or instead detect patterns in training data and build a predictive model? (instance-based vs. model-lbased learning)

### Supervised learning algorithms

* k-nearest neighbors
* Linear regression
* Logistic regression
* SVMs
* Decision trees and ensembles
* Neural networks

### Unsupervised learning algorithms

* Clustering (K-means, DBSCAN, hierarchical cluster analysis)
* Anomaly detection and novelty detection (one-class SVM, isolation forest)
* Visualization and dimensionality reduction (PCA, kernel PCA, locally linear embedding, t-SNE)
* Association rule learning (apriori, eclat)

Dimensionality reduction:
* Goal: simplify the data without losing too much information
* One way is to merge several correlated features into one (_feature extraction_). For example, a car's mileage may be strongly correlated with its age, so dimensionality reduction will merge them into one feature that represents the car's wear and tear. 
* Often a good idea to apply dimensionality reduction to training data before feeding to another ML algorithm (like supervised learning) - smaller memory, faster training, sometimes better performance

Anomaly detection:
* Ex: detecting unusual cc transactions to prevent fraud, catching manufacturing defects, automatically removing outliers from a dataset before feeding it to another learning algorithm
* Show mostly normal instances during training so system learns to recognize them and can predict if a new sample is normal or anomalous
* Novelty detection: more extreme version of anomaly detection where novelty is detected only if the sample is not represented AT ALL in the training set

Association rule learning:
* Discover interesting relations b/w attributes in dataset
* E.g. you own a supermarket and find that people who buy barbecue sauce and potato chips also tend to buy steak, so you should place them close together

### Semisupervised learning algorithms

For data that's partially (mostly) unlabeled.

Most semisupervised learning is a combo of unsupervised and supervised, e.g. deep belief networks (DBNs) are based on restricted Boltzmann machines (RBMs).

### Reinforcement learning

The learning system is called an agent.
* Observes the environment
* Selects and performs actions (based on its policy)
* Gets rewarded (or penalized)
* Updates policy (learning step)

The agent learns the best strategy, called a policy, to get the most reward over time. A policy defines what action the agent should choose in any given situation.

E.g. robots, AlphaGo.

### Batch and online learning

### Instance-based vs. model-based learning

I think this is parametric and non-parametric learning.

## Main challenges of ML

Task: select algo, train on data.

What can go wrong? Bad algo or bad data.

### Insufficient quantity of training data

Even for simple problems, you typically need thousands of examples.

For complex problems, you may need millions (unless you reuse parts of an existing model, i.e. transfer learning).

Research papers have shown that as dataset size increases, algorithm complexity becomes less important. That is, for large datasets, different algorithms - simple or complex - have almost the same performance.

However, it's not always easy or cheap to get training data, so it's still important to know algorithms.

### Nonrepresentative training data

It is crucial to use a training set that is representative of the cases you want to generalize to.

If the sample is too small, you will have _sampling noise_ (nonrepresentative data due to chance), but even very large samples can be nonrepresentative if the sampling method is flawed (_sampling bias_).

### Poor-quality data

Errors, outliers, and noise will make it difficult for the system to detect the underlying patterns, so it'll likely perform poorly.
* You may want to discard outliers or fix them manually
* Missing values - you must decide if you want to ignore the attribute altogether, ignore these instances, fill them in, or train one model with the feature and one without the feature

### Irrelevant features

Feature engineering steps:
* Feature selection (selecting the most useful features to train on)
* Feature extraction (combining existing features to produce a more useful one, e.g. with dimensionality reduction algorithms)
* Creating new features by gathering new data

### Overfitting the training data

Complex models can detect subtle patterns in data, but if the training set is noisy or too small (sampling noise), then the model is likely to detect patterns in the noise itself. Obviously these patterns will not generalize to new instances.

For example, if you want to predict life satisfaction per country, what if you included the country name as a feature? This feature contains zero information but the model may pick up on something that isn't real.

Overfitting occurs when the model is too complex relative to the amount and noisiness of training data. You can
* Simplify the model: fewer parameters, reducing the training data dimension, or constraining the model (regularization)
* Gather more training data
* Reduce training data noise (fix errors and outliers)

Regularization example: let's say we have two parameters, theta0 and theta1. We have two degrees of freedom. If we force theta1 = 0, then we have one degree of freedom. If we force theta1 to be small, then we have somewhere between one and two degrees of freedom. You want to find the right balance b/w fitting the training data perfectly and keeping the model simple enough to generalize well.

### Underfitting the training data

Model too simple to learn the underlying structure/patterns of data.

Fixes:
* Select more powerful model, with more parameters
* Feed better features to the learning algorithm (feature engineering)
* Reduce model constraints (e.g. reduce regularization)

## Testing and validation

Error rate on new samples is called generalization error or out-of-sample error, and by splitting your training data, you can estimate this error rate.

Common train-test split is 80-20, but for very large datasets this can be 99-1.

### Hyperparameter tuning and model selection

You split data into train and test. You run hyperparameter tuning and select the model with the lowest generalization error on the test set. However, in production, the generalization error is much higher.

The problem is that you adapted the model and hyperparameters to produce the best model on your specific test set. This makes the model less likely to perform well on new data.

A common solution is _holdout validation_: hold out part of the training set for hyperparameter tuning (validation or development set). Select hyperparameters based on validation set performance, retrain on entire training set (no hold out), and estimate generalization error on the test set.
* If validation set is too small, then model evaluations will be imprecise, and you might select a suboptimal model
* If validation set is too large, then you have less training data, which would impact the actual training of the model parameters

Then you can try _cross validation_: by averaging over many validation sets, you get a more accurate measure of performance (at the cost of increased training time).

### Data mismatch

Between training data and production data.

You have millions of training data that you've collected from the web, and 10000 examples that you've collected from your deployed application. These are representative examples. You do not know if your training examples are representative.

Validation and test sets must be as representative as possible of the data you expect to use in production (making sure no duplicates or near-duplicates end up in both sets), so you set aside all 10000 representative examples for them.

You train your model and evaluate on the validation set. Performance is low. Is your model overfitting? Or is there a training-validation data mismatch?

In this case, you can hold out some of the training examples into another set that Andrew Ng calls the train-dev set. Train again and evaluate on train-dev set. 
* If performance is good, then the model is not overfitting. That means there is a data mismatch you need to address (perhaps by augmenting/preprocessing the training samples).
* If performance is still bad, then the model is overfitting (simplify/regularize the model, collect more training data, clean up training data).

# Chapter 2 End-to-end ML project

## Look at the big picture

### Frame the problem

**What is the business objective? (It's not building a model).**

**A note on data pipelines:**

Let's say the output of your model - its prediction - will be fed into a downstream ML system.

A sequence of data processing components - including ML models - is called a _data pipeline_. Pipelines are very common since there is a lot of data to manipulate and many data transformations to apply.

Components typically run asynchronously. 
* Each component pulls in a large amount of data, processes it, and spits out the result in another data store. Some time later, the next component does the same thing. 
* Each component is fairly self-contained: the interface between components is the data store. This modularity simplifies the system architecture and allows for different teams to focus on different components.
* If a component breaks down, the downstream components can often continue to run normally (at least for a while), which makes the architecture robust.
* However, if a broken component goes unnoticed because proper monitoring isn't implemented, then the data gets stale and the system performance drops.

**What is the current solution/implementation?**

This will give you a reference on performance, as well as insights on how to solve the problem.

**Now, the ML questions:**
* Does this require supervised, unsupervised, or reinforcement learning?
* Classification, regression, something else?
* Batch learning or online learning?

### Select a performance measure

### Check the assumptions

List and verify the assumptions that have been made so far to make sure you're working on the correct problem.

## Initial look at the data (univariate analysis)

Understand the data. Ask the simple questions:
* What are the scales?
* How was it preprocessed? 
* Are there missing values?

Run simple univariate analysis and visualization (histograms and bar charts). How are the attributes distributed?

Are any of the answers to these questions going to be a problem? Do you need to collect more data? Clean up the data? Transform the data? Keep this in mind for later.

## Create the test set

DO NOT LOOK AT THE TEST SET. If you see something in the test set that informs your model selection, your performance will be biased to the test set. This is called _data snooping_ bias.

Creating the test set with purely random sampling:
* If your dataset doesn't change, you can simply set the random seed so that the test split is the same every time, or you can save the test set. This guarantees your test set doesn't change.
* If your dataset can be updated, a common solution is to use each sample's identifier to split (assuming samples have unique and immutable IDs or you can create one). E.g. compute a hash of each ID and funnel the sample to the test set if its hash is < 20% (test ratio) of the max hash value.

Purely random sampling can be problematic if your dataset is not large relative to the number of attributes because you risk introducing sampling bias.

In _stratified sampling_, you curate your dataset to be representative of the population, which is split into homogeneous subgroups called strata. This means the dataset, w.r.t. the attribute of interest, will have the same distribution as the population. When the distribution of the dataset does not match the population, it is said to be _skewed_.

To stratify along a continuous attribute, you need to convert it to categorical first (you can use `pd.cut`). It is important to have a sufficient number of instances in your dataset for each stratum, otherwise the estimate of a stratum's importance may be biased.

Some dataset splitting options from `sklearn.model_selection`:
* `train_test_split`
* `KFolds`
* `StratifiedKFold`
* `ShuffleSplit`
* `StratifiedShuffleSplit`

## Closer look at the data (multivariate analysis)

In this part, only look at the training set.

The point of this part is to look for patterns yourself, and you will probably need to play around with visualization parameters to make the patterns stand out. For example, for scatter plots,
* `alpha` parameter adjusts the transparency of the points, which is useful for analyzing density
* Set marker size based on attribute value
* Choose marker color based on attribute value and use the color map option to indicate scaling (e.g. blue for low values to red for high values)

Calculate correlations between every pair of attributes using `df.corr()`. Pay special attention to correlations with the target attribute. You will want to pay attention to features that are strongly correlated with the target.

Correlation coefficient only measures linear correlations - it cannot capture nonlinear relationships. Furthermore, correlation coefficient is independent of slope. A linear relationship can have any slope but only +/-1 correlation. That's why we need scatter plots.

Note: Of course you want to find patterns that will inform your model choice. However, also pay attention to patterns in the data that may degrade your model performance.

### Experimenting with attribute combinations

At this point, you will have identified
* Data to be cleaned
* Correlations, especially with the target
* Skewed distributions that you may want to transform

You may be able to create more discriminative features from the raw features. For example, creating a new feature that is a ratio of two raw features is an operation that cannot be learned by a linear model.

This process does not need to be absolutely thorough - you will come back to this again and again during the ML lifecycle.

## Preparing the data for ML algorithms

Use functions so you can easily reproduce the transformations on any dataset, any future project, and on the live system.

Modular functions will allow you to easily try various transformation pipelines.

