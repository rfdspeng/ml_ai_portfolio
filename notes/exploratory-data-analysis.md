# Look up/quick notes
https://medium.com/data-science/a-data-scientists-essential-guide-to-exploratory-data-analysis-25637eee0cf6

data smell, code smell

For correlated features or features that are linear combinations of other features (linear algebra) - can you use linear algebra to scrap dependent features? Is correlation coefficient enough? How are these related?

# Data types in data science

https://builtin.com/data-science/data-types-statistics

Data in data science is broadly classified into qualitative vs. quantitative:
* Qualitative = Categorical (cannot be measured numerically)
    * Nominal: no inherent order or ranking (e.g. colors, gender, yes/no)
    * Ordinal: meaningful order or ranking (e.g. survey responses from strongly disagree to strongly agree)
* Quantitative = Numerical
    * Discrete (e.g. number of students in a class)
    * Continuous (e.g. height, temperature, weight)
* Others

# Step 1: Data overview and descriptive statistics

The process is different for different types of datasets:
* Tabular: num observations, num and types of features (numerical, categorical), missing rate, duplicates
* Time series
* Text, image, video

For tabular:
```python
# Dataset Overview
df.head() # preview a sample
df.shape  # number of observations and features
df.dtypes # data types
df[df.duplicated()] # check duplicated rows
df.isna().sum() # missing values per feature
df.isna().sum().sum() # number of missing cells
round(df.isna().sum().sum() / df.size * 100, 1) # percentage of missing cells
df.describe() # numerical only
df.describe(include="object") # for categorical data types
```



# Step 2: Feature assessment and visualization

Understand the feature properties, both individually (univariate analysis) and their interactions and relationships (multivariate analysis). 

We need to investigate the sufficient statistics and visualize the features.

A sufficient statistic is a statistic that contains all the information in the sample regarding a specific parameter (a summary statistic that doesn't lose any relevant information). It doesn't depend on the parameter.

## Univariate analysis

Informs us of the relevance of each feature and the type of data prep required.
* Look for inconsistencies or outliers
* Standardize numerical features if needed
* Encode categorical features
* Handle shifted or skewed numerical features if the ML algorithm we want to use expects a particular feature distribution

Descriptive stats and visualizations:
* Numerical features: mean, standard deviation, skewness, kurtosis, quantiles; best represented using histograms
* Categorical features: mode, frequency table; represented using bar plots

If a feature is constant or nearly constant, then it may not be valuable for analysis or modeling.

However, it depends on the feature. If the feature should be a strong predictor but has an imbalanced distribution, then the learning algorithm will overlook the less represented feature values (e.g. if race is a feature but the dataset mostly contains data about white people). This is known as the problem of small disjuncts and leads to reduced learning performance.

Small disjuncts may have consequences for bias and fairness.

We should consider performing data augmentation conditioned on the underrepresented categories and consider fairness-aware metrics for model evaluation.

## Multivariate analysis

Interactions: visually explore how each pair of features behaves. They may exhibit positive or negative relationships. Essentially a 2D scatter plot.

Correlations: quantify the relationship by calculating correlation coefficients/matrix and by visualizing the matrix as a heatmap where x and y axes are features and correlation between features is indicated on a color scale.

Correlation calculation (default option for `ydata-profiling`):
* Numeric feature vs. numeric feature: Spearman's rank correlation coefficient
* Categorical vs. categorical: Cramer's V
* Numeric vs. categorical: Cramer's V with the numeric feature discretized

Remove redundant features if possible.

Knowing the most correlated features to our target class helps us identify the most discriminative features and find possible data leakers.

## Discriminative features

## Data leakage

# Step 3: Data quality evaluation

This step follows from the previous two.

Data quality issues: Missing data, imbalanced data, constant values, duplicates, highly correlated or redundant features, noisy data, etc.

Read more: https://towardsdatascience.com/data-quality-issues-that-kill-your-machine-learning-models-961591340b40/

Errors may occur during data collection or processing.

## Data leakers