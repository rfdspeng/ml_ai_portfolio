# What is machine learning? Why use machine learning?

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

# Example applications

* Image classification, semantic segmentation -> CNNs
* Text classification, summarization, speech recognition, and anything involving sequences -> RNNs, CNNs, transformers
* Regression -> linear or polynomial regression, regression SVM, regression random forest, ANN
* Anomaly detection
* Clustering (e.g. segmenting clients based on purchases so you can design a different marketing strategy for each segment)
* Data visualization of high-dimensional datasets, often involving dimensionality reduction techniques
* Recommender systems -> train ANN on history of past purchases to get most likely next purchase
* Reinforcement learning to train agents (such as bots) to maximize rewards over time

# Types of ML systems

Broad classifications:
* Trained with human supervision? (supervised, unsupervised, semisupervised, reinforcement learning)
* Can learn incrementally on the fly? (online vs. batch learning)
* Compare new data points to known data points or instead detect patterns in training data and build a predictive model? (instance-based vs. model-lbased learning)

## Supervised learning algorithms

* k-nearest neighbors
* Linear regression
* Logistic regression
* SVMs
* Decision trees and ensembles
* Neural networks

## Unsupervised learning algorithms

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

## Semisupervised learning algorithms

For data that's partially (mostly) unlabeled.

Most semisupervised learning is a combo of unsupervised and supervised, e.g. deep belief networks (DBNs) are based on restricted Boltzmann machines (RBMs).

## Reinforcement learning

The learning system is called an agent.
* Observes the environment
* Selects and performs actions (based on its policy)
* Gets rewarded (or penalized)
* Updates policy (learning step)

The agent learns the best strategy, called a policy, to get the most reward over time. A policy defines what action the agent should choose in any given situation.

E.g. robots, AlphaGo.

## Batch and online learning

