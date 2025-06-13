# Look up/quick notes
https://medium.com/data-science/a-data-scientists-essential-guide-to-exploratory-data-analysis-25637eee0cf6

https://www.youtube.com/watch?v=xi0vhXFPegw

Hands on machine learning (book)

data smell, code smell

For correlated features or features that are linear combinations of other features (linear algebra) - can you use linear algebra to scrap dependent features? Is correlation coefficient enough? How are these related?

Using linear algebra for EDA

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

Approach every dataset with suspicion. DO NOT TRUST THE DATASET.

What are the questions we should be asking of the dataset?

For tabular data:
```python
"Preview the dataset"
pd.set_option(display.max_columns, 200)
df.head()
df.tail()
df.sample()

"""
Understand the dataset
* How many observations (samples)? How many features?
* What are the names of our features?
* What are the data types of our features?
* Quick statistical overview of our features
"""
df.shape # (num samples, num features)
df.size # num samples * num features (total entries)
df.columns # feature names
df.dtypes # data types
df.info()
df.describe() # numerical stats
df.describe(include="object") # categorical stats

"""
Preparing the data
* Do we need all of the features? Drop the features we don't need.
* Are the features the correct data type? Do we need to convert any data types?
* Are there any missing values? How do we handle missing values?
* Are there any duplicate samples? Which features should we check for duplicates? Do we want to remove them?
"""
df_new = df.drop([columns], axis=1) # returns a copy with columns dropped
df_new = df[[columns]].copy() # equivalent using subsetting
infer_objects
pd.to_numeric(series)
pd.to_datetime(series)
pd.to_timedelta()
convert_dtypes
astype
df.isna() # DataFrame with True/False 
df.isna().sum() # Series; number of missing entries per column
df.isna().sum().sum() # Total number of missing entries
round(df.isna().sum().sum() / df.size * 100, 1) # percentage of missing cells

dropna
fillna



df.loc[df.duplicated()] # check duplicated rows
df.loc[df.duplicated(subset=[columns])] # check for duplicates for a subset of columns
df_new = df.loc[~df.duplicated(subset=[columns])] # retain non-duplicates

```

Handling missing values - either
* Omission (remove samples w/missing values). Use when
    * Small number missing
    * Missing values are completely at random (MCAR) so that removing them won't change the feature distribution. If you identify patterns of missing data, then this is information you should not remove.
    * If feature is missing most of its values, them remove it entirely
* Imputation (infer missing values)
    * Fill with default values, which depends on dtype, e.g. for numerical, mean/median; for categorical, default choice
    * For numerical data that is taken over time or over geographic region, you can interpolate
    * Train a supervised model to fill missing values based on other features
    * 




# Step 2: Feature assessment and visualization

Understand the feature properties, both individually (univariate analysis) and their interactions and relationships (multivariate analysis). 

We need to investigate the sufficient statistics and visualize the features.

A sufficient statistic is a statistic that contains all the information in the sample regarding a specific parameter (a summary statistic that doesn't lose any relevant information). It doesn't depend on the parameter.

## Questions to ask yourself

Be aware of how your data (features and labels, i.e. attributes) was collected. Data often have already been preprocessed, e.g. a numerical feature may have been clipped to min/max values.

What are the scales of the data? What kind of preprocessing was done?

Is this preprocessing acceptable? Do you need to handle it in some way - either recollecting data or removing the offending attributes?

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

For tabular data:
```python
"""
Running simple descriptive statistics to understand our data distribution
What kinds of questions should we be asking? Look for outliers, skew, ?
* Numerical stats, categorical stats
"""
df[col].value_counts()
ax = df[col].value_counts().head(10).plot(kind="bar", title="title")
ax.set_xlabel("x")
ax.set_ylabel("y")
plot(kind="hist", bins=n, title="title")
plot(kind="kde") # density plot (normalized and smoothed hist?)
plot(kind="barh")
```

## Multivariate analysis

Interactions: visually explore how each pair of features behaves. They may exhibit positive or negative relationships. Essentially a 2D scatter plot.

Correlations: quantify the relationship by calculating correlation coefficients/matrix and by visualizing the matrix as a heatmap where x and y axes are features and correlation between features is indicated on a color scale.

Correlation calculation (default option for `ydata-profiling`):
* Numeric feature vs. numeric feature: Spearman's rank correlation coefficient
* Categorical vs. categorical: Cramer's V
* Numeric vs. categorical: Cramer's V with the numeric feature discretized

Remove redundant features if possible.

Knowing the most correlated features to our target class helps us identify the most discriminative features and find possible data leakers.

```python
"""
What are the relationships between our features?
* Use scatter plots
* Calculate correlations between features
"""
df.plot(kind="scatter", x=col1, y=col2)
plt.show() # for cleaning notebook output (do not want to display object)
sns.scatterplot(x=col1, y=col2, hue=col3, data=df) # color the dots based on col3; adds a third dimension to the plot
sns.pairplot(data=df, vars, x_vars, y_vars, hue=hue_col, kind="scatter") # 2D plots for multiple pairs of features
df_corr = df.corr() # correlation matrix
sns.heatmap(df_corr, annot=True) # heatmap of correlation matrix


```

Ask a question about the data. Try to answer the question using plots and statistics.
```python
df.query().groupby()[col].agg([]).query().sort_values(sort_col).plot()
```

## Discriminative features

## Data leakage

# Step 3: Data quality evaluation

This step follows from the previous two.

Data quality issues: Missing data, imbalanced data, constant values, duplicates, highly correlated or redundant features, noisy data, etc.

Read more: https://towardsdatascience.com/data-quality-issues-that-kill-your-machine-learning-models-961591340b40/

Errors may occur during data collection or processing.



## Data leakers