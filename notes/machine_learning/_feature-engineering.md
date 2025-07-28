# Numeric data

Good features should not only represent salient aspects of the data, but also conform to the assumptions of the model - transformations are often necessary. Numeric feature engineering techniques are fundamental.
* Does magnitude matter? Or do we only need to know positive/negative? Or do we only need to know magnitude at very coarse granularity?
* Consider the scale of the features. What are the largest and smallest values? Do they span several orders of magnitude? 
    * Models that are smooth functions of input features are sensitive to the scale of the input, e.g. linear regression, k-means clustering, nearest neighbors, radial basis function (RBF) kernels, and anything that uses Euclidean distance. For these models, it's often a good idea to normalize the features so the output stays on the expected scale.
    * Logical functions are not sensitive to input feature scale - their output is always binary. This includes step functions (e.g. is input greater than 5?). This is why models based on space-partitioning trees (decision trees, gradient-boosted machines, random forests) are not sensitive to scale. The only exception is if the scale of the input grows over time and grows outside of the range the tree was trained on.
* The distribution of a numeric feature matters for some models. For example, linear regression assumes that prediction errors are Gaussian. Log transforms, a type of power transform, can transform the distribution of a feature closer to Gaussian.

Depending on your answers to the previous questions, you may
* Keep data as raw numbers
* Convert them into binary values to indicate presence
* Bin them into coarser granularity
* Apply a log transformation


## Binarization

Example: we want to build a song recommender, and we have song listen counts for users. If this is our target, the raw listen count may not be a robust measure of user taste since users have different listening habits. (Some users may listen to songs on repeat, some users might listen to music all day, etc.)

(Robustness means that the method works under a wide variety of conditions.)

To create a more robust measure, we might clip counts to a maximum of 1 so that the feature takes on only values of 0 and 1. (Technically, this is target engineering.)

## Quantization (aka binning)

Features that span several orders of magnitude are problematic for many models. In a linear model, the same coefficient needs to work for all possible values. In k-means clustering, an exceptionally large value in a feature might dominate all other features (and drown out their information).

Binning is one way to reduce range. Group the feature into bins and map the raw data into bin numbers, thereby converting from continuous to discrete. There are two approaches, fixed-width binning and adaptive binning.

### Fixed-width binning

Each bin contains a specific numeric range. Bins can be custom or automatically segmented, linearly or exponentially scaled.

To automatically segment into linearly scaled bins, divide raw number by desired binwidth and take floor. For example, if binwidth is 10, then the bins correspond to 0-9, 10-19, 20-29, etc.

To automatically segment into exponentially scaled bins, take the log of the raw number and take floor. For example, with log10, the bins correspond to 0-9, 10-99, 100-999, 1000-9999, etc. This may be better for features that span several orders of magnitude. This is very much related to the log transform.

### Adaptive binning (using quantiles)

If there are large gaps in the range of numbers, then there could be many empty bins with no data. We can solve this by adaptively positioning the bins based on the distribution of the data.

For examples, you could split the feature into 10 bins by splitting by deciles.

You can use `pandas.DataFrame.quantile` and `pandas.Series.quantile`. `pandas.qcut` maps the data into a desired number of quantiles.

## Log transformation

log_a(a^x) = x

Log function maps (0, 1] to (-infinity, 0].

log10 maps 
* [1, 10] -> [0, 1]
* [10, 100] -> [1, 2]
* [100, 1000] -> [2, 3]

In other words, log function compresses the range of large numbers and expands the range of small numbers. This makes it a powerful tool for dealing with positive numbers with a heavy-tailed distribution - at the high end, it compresses the long tail into a shorter tail, and expands the low end into a longer head.

🧮 1. Handling log(Fare) with zero values

    Problem: Some rows have Fare = 0, and log(0) is undefined (returns -inf).

✅ Recommended approaches:
Option A: Add a small constant (log1p-like trick)

df['LogFare'] = np.log(df['Fare'] + 1)

    This shifts the scale slightly but keeps relative ordering.

    It's equivalent to np.log1p(Fare), which is numerically stable for small values.

Option B: Replace 0s with NaN or small positive value

df['Fare_cleaned'] = df['Fare'].replace(0, np.nan)
df['LogFare'] = np.log(df['Fare_cleaned'])

You can impute the zero-fare values later based on domain knowledge (e.g., passengers in 3rd class may have been granted free fares).
Option C: Leave it untransformed, or bucket it

If the transformation adds complexity but doesn’t help with separability, consider:

    Binning into fare brackets (e.g., low/medium/high)

    Using quantiles: pd.qcut(df['Fare'], q=4)