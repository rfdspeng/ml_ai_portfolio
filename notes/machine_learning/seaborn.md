# Introduction

* A library for making statistical graphics
* Builds on top of matplotlib
* Integrates with pandas - dataset-oriented, declarative API
* Many functions automatically perform statistical estimation and compute confidence intervals
* Plot numerical and categorical variables; plot relationships between variables; provides figure- and axes-level plotting functions
* Recommended to use matplotlib for polishing plots to publication quality

# Overview of plotting functions

## Relational, distributional, categorical modules

There are three main modules - relational, distributional, categorical.

Each contains functions with similar visualization goals:
* Relational: visualize relationship between two numerical variables
* Distributional: visualize distributions of numerical variables
* Categorical: visualize categorical variables

Each module contains a figure-level function and axes-level functions. It's recommended to use figure-level functions unless you need to compose a complex, standalone figure that composes multiple different plot kinds. In that case, set up a figure using matplotlib (`plt.subplots`) and use axes-level functions to fill in the subplots (by passing axes into `ax`).

Functions (first is figure-level)
* Relational: `relplot`, `scatterplot`, `lineplot`
* Distributional: `displot`, `histplot`, `kdeplot`, `ecdfplot`, `rugplot`
* Categorical: `catplot`, `stripplot`, `swarmplot`, `boxplot`, `violinplot`, `pointplot`, `barplot`

Figure-level functions:
* Return a `FacetGrid` that can be used to manage the figure. See API for methods (like `set_axis_labels`).
* Easily create figures with multiple subplots that are split by categorical variables using `col` and `row`
* Wraps around axes-level functions. Specify plot type with `kind`. Pass kind-specific keywords.
* Access axes via `FacetGrid.ax` or `FacetGrid.axes` for multiple subplots
* Unlike matplotlib, you don't specify the figure size - each subplot created by the figure-level function has the same size (so figure size automatically scales). Instead, you specify `height` and `aspect`.

|Advantages|Drawbacks|
|----------|---------|
|Easy faceting by data variables|Many parameters not in function signature|
|Legend outside of plot by default|Cannot be part of a larger matplotlib figure|
|Easy figure-level customization|Different API from matplotlib|
|Different figure size parameterization|Different figure size parameterization|

## Combining multiple views on the data

`jointplot` and `pairplot` are outside of the three modules described above - they employ multiple kinds of plots from different modules.

Use them for visualizing bivariate (joint) and univariate (marginal) distributions of numerical variables. Both are figure-level functions and create figures with multiple subplots by default.

`jointplot`: plot the relationship between two variables along with their marginal distributions. Comes with several canned plot kinds - if you need more flexibility, use `JointGrid` directly.

`pairplot`: same as `jointplot` but plots bivariate distributions for all pairs of variables in the dataset

`jointplot` returns `JointGrid` and `pairplot` returns `PairGrid` for managing the figure.

# Visualizing statistical relationships (relational module)

## Scatterplots and lineplots

`relplot` combines a `FacetGrid` with one of two axes-level functions:
* `scatterplot` (default)
* `lineplot`

These functions plot the joint distribution of two numeric variables. You can add three additional variables to the visualization by passing `hue`, `size`, and `style` (although it may not be a good idea to do this, since you may lose visual meaning). This is called semantic mapping.
* `hue` may be categorical or numeric (switches between qualitative and sequential palette) - changes marker/line color
    * You can and probably should specify `palette`
* `style` is always treated as categorical - changes marker/line style. For line plots, you can enable marker style over line style with `dashes=False, markers=True`.
* `size` may be categorical or numeric - changes marker/line size. The raw values of the size variable are normalized into a range, but the range is customizable via `sizes`.

Even if you add only one additional variable, it's good practice to use that variable for both `hue` and `style`.

Example: `sns.relplot(my_dataframe, kind="scatter", x="x_col", y="y_col", hue="hue_col", style="style_col", size="size_col", sizes=(15, 200))`

Line plots are better when `y` is a function of time or another similarly continuous variable.

Example: `sns.relplot(my_dataframe, kind="line", x="time", y="money", hue="hue_col", style="style_col", size="size_col", sizes=(15, 200))`

## Statistical aggregation for line plots

If your data has multiple measurements for the same `x`, then for a given `x`, `y` is a random variable with some distribution. In addition to mean, `lineplot` can visualize the spread of that distribution using `errorbar`.

Valid arguments for `errorbar`:
* `"ci"` - confidence interval (computed using bootstrapping)
* `"pi"` - percentile interval (computed using bootstrapping)
* `"se"` - standard error
* `"sd"` - standard deviation
* Tuple: (one of the above methods, level parameter). Examples:
    * `("ci", 99.7)`
    * `("pi", 50)`
    * `("se", 3)`
    * `("sd", 2)`
* A function that maps from a vector to a (min, max) interval
* `None`: turns off the error bar

For more on error bars, see the section on statistical estimation and error bars.

If you want to turn off statistical aggregation entirely, set `estimator` to `None`. This might produce a strange effect if you have multiple observations per `x`. However, if the multiple observations corresponds to different subjects, you can pass the column that defines the subjects to `units`, which will draw one curve per subject.

## Showing multiple relationships with facets

Using semantic mapping with too many variables can decrease the readability of your plots. When this is the case, it's better to make multiple plots by faceting on columns and rows.

Faceting allows you to make multiple plots of the x-y relationship conditioned on categorical variables.

For example, if you set `col="Sex"` and `row="Class"`, then each subplot is conditioned on a unique sex-class group. It's like a groupby operation for visualization.

If your facet variable has many categories, you may want to facet on columns and then "wrap" the facets into rows using `col_wrap`.

This visualization technique is also called "lattice" plots or "small-multiples".

# Visualizing distributions of data (distributional module)

This module is primarily for numeric variables (discrete and continuous). You can visualize univariate and bivariate distributions.

`displot` is the figure-level function that wraps around `histplot`, `kdeplot`, `ecdfplot`, and `rugplot`. `ecdfplot` is univariate only; the others can visualize bivariate.

`jointplot` and `pairplot` wrap `histplot` and `kdeplot`.

Distributions support `hue` semantic and faceting by `col` and `row`.

Histograms:
* `binwidth`
* `bins` - specify number of bins or a list of bin breaks
* `discrete=True` for discrete variables
* `element` - specify bar graphic
* `stat` - normalize histogram
* `kde` - draw KDE. Use `kde_kws` to pass KDE options, e.g. `{"bw_adjust": 1}`.

Kernel density estimation:
* `bw_adjust` - smoothing parameter
* KDE assumes the underlying distribution is smooth and unbounded. It is not a good representation for jagged and/or bounded data.

Empirical cumulative distributions:
* Unlike histogram and KDE, it directly represents each datapoint - no bin size or smoothing parameter to consider
* Good for comparing multiple distributions (e.g. using `hue`)
* Less intuitive visualization of the distribution shape compared to histogram/KDE

Visualization options when using `hue` semantic mapping:
* `multiple` - specify how to display multiple histograms
* `common_norm` - how to normalize multiple histograms

## Visualizing bivariate distributions

Primarily using histograms and KDE. Pass `x` and `y`.

Histograms do 2D binning and colors each rectangle based on count (like a heatmap). Set `cbar=True` to aid visual interpretation.

One or both histogram variables can be discrete.
* One discrete variable: another way to plot conditional univariate distributions (of the continuous variable)
* Both discrete variables: cross-tabulation visualization

KDE smoothes (x, y) with a 2D Gaussian and plots the contours of the 2D density. Each curve shows a level set s.t. some proportion of density lies below it. Specify levels via `thresh` and `levels`.

Binning and smoothing still applies. Pass a pair of values (e.g. a 2-ple) to specify per variable.

Generally, `hue` semantic mapping works better with 2D KDE. It only works with 2D histograms if there is minimal overlap between conditional distributions.

## `jointplot`, `pairplot`

`jointplot` and `pairplot` wrap `histplot` and `kdeplot`.



# Visualizing categorical data

# Statistical estimation and error bars



# Estimating regression fits

# Building structured multi-plot grids

# Data structures accepted by seaborn

Generally I think I'll be using long-form data (pandas dataframes).

# Properties of Mark objects

# Choosing color palettes