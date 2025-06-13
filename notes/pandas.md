# Resources
* Kaggle pandas tutorial
* pandas API reference
* https://www.youtube.com/watch?v=DkjCaAMBGWM
* https://www.youtube.com/watch?v=_gaAoJBMJ_Q

# Quick tips
* `pd.set_option('display.max_columns', 500)`
* `df.head()`, `df.tail()`, `df.sample(5)`, `df.sample(frac=0.1)`
* `df.columns`, `df.index`
    * `df.columns[slice object]`
    * `[c for c in df.columns if (some condition)]`
* `df.info()` - columns, data types, memory usage
* `df.info(verbose=False)`
* `df.describe()` - basic stats for both numerical and categorical
* `df.shape`
* `df.select_dtypes(data type)` - select columns with data type
* `df/series.copy()` - make a copy so you don't corrupt the original
* `df.to_csv(fname, index=False)` - do not save index if it's not useful
* `df.read_csv(fname, parse_dates=[column])` - read in from CSV with correct dtype
* Save to different file types - CSV is very slow, and other file types retain dtype. `to_parquet`, `to_feather`, `to_pickle`.
* Do not use column names with spaces - cannot access columns via dot syntax, harder to `query` columns
* `query` is a powerful way to filter DataFrames (over using conditional indexing)
* In `query`, use the syntax `@var_name` to access external variables
* Do not use use the inplace option
* Do not use loops to iterate over columns - use vectorized operations
* Do not use `apply` or `map` if you can use vectorized operations
* A slice of a DataFrame does not create a copy - use `copy` to create a deep copy of a slice
* Use method chaining instead of temporary variables
    * Wrap code in parentheses for readability, e.g.
    ```python
    df_agg = (
        df
        .groupby()
        .min()
        .reset_index()
        .fillna(0)
        .sort_values()
    )
    ```
* Use pandas built-in plotting methods
* Use pandas built-in string methods: `series.str.<string-command>`
* `series.pct_change()` - calculate percentage change from entry to entry
* `series.diff()` - calculate diff of entries
* Pandas has built-in conditional formatting (like Excel) using `df.style` attribute, e.g. `df.style.background_gradient`, `df.style.format`
* Store categorical variables as categorical dtype using `series.astype('category')` - smaller memory and faster operations


# Supported data types

"object" refers to any Python object

filter columns on dtype

# DataFrames and Series

Two data structures, DataFrames and Series. DataFrame is a bunch of Series (columns) glued together.

Be aware of whether DataFrames or Series are returned by operations, and be aware of whether a copy is returned.

Construction:
```python
new_df = pd.DataFrame({"col1_header":[entries], "col2_header": [entries]}, index=[row labels])

new_series = pd.Series([entries], index=[row labels])

df.index # get row labels
df.columns # get column names

df = pd.read_csv(filename, index_col=0) # index_col=0 means use the first column as the index
```

Can read in many different file types. `read_csv` is the most common. Options to be aware of: delimiter, usecols (read subset of columns), parse_dates, chunksize (reading large files in chunks).

Can write to many different file types and database (to_sql).

## Attributes

`shape`

# Indexing (subsetting), selecting (filtering), assigning

Columns are properties of DataFrames. You can access like an attribute or by using the indexing operator. AKA subsetting.
```python
df.col
df[col] # Returns Series
df[[cols]] # Returns DataFrame
```

This is fine for simple cases and only when you want to index (never for assignment). You should generally use `df.loc()` and `df.iloc()` instead. AND YOU SHOULD NEVER CHAIN INDEX, AND CERTAINLY NOT FOR ASSIGNMENT. https://pandas.pydata.org/pandas-docs/version/0.22/indexing.html#indexing-view-versus-copy


`iloc` is position/index-based selection. `loc` is label-based selection.

`iloc` uses Python stdlib indexing scheme, where the first element of the range is included and the last one is excluded, i.e. `0:10` returns 0,...,9.

`loc` indexes inclusively, so `0:10` returns 0,...,10.

## Label-based selection and assignment with loc

Rows/cols may be
* Single label
* List of labels
* A slice object of labels (including string slice objects)
* A boolean array of the same length as the axis being sliced
* An alignable boolean Series
* An alignable `Index`
* A callable function with one argument (the calling Series or DataFrame) that returns valid output for indexing (one of the above)
```python
# df.loc[rows, cols]

df.loc[index] # Returns row as a Series
df.loc[[ind1, ind2, ...]] # Returns DataFrame. Using [] always returns a DataFrame even if the list contains 1 element.
df.loc[ind, col] # Returns element
df.loc[[ind0:indN], col]
df.loc[[False, False, True]]
df.loc[pd.Series([False, True, False], index=[indices of df])] # Alignable boolean Series
df.loc[pd.Index([indices])]
df.loc[df[col] > 5] # Conditional that returns a boolean Series
df.loc[df[col] > 5, [col1]]
df.loc[(df[col1] > 5) & (df[col2] == 2)] # Multiple conditional (wrap conditions in parentheses)
df.loc[(df[col1] > 5) | (df[col2] == 2)] # Multiple conditional (wrap conditions in parentheses)
df.loc[~condition] # NOT
df.loc[lambda df: df[col] == 5] # Callable that returns a boolean Series
df.loc[df.col.idxmax()] # Get row where col has its first occurrence of max value

# Built-in conditional selectors
df.loc[df[col].isin([list of values])]
df.loc[df[col].notnull()]
df.loc[df[col].isnull()]

df.loc[[indices], [columns]] = 50 # Set all items matching list of labels
df.loc[index] = 50 # Set value for entire row
df.loc[:, col] = 50 # Set value for entire column
df.loc[df[col] > 35] = 0 # Set value for rows matching callable condition
df.loc[ind, col] += 5
df.loc[ind] = [any iterable of the same length]
df.loc[:, col] = [any iterable of the same length]

# Setting using a Series or DataFrame sets the values matching the index labels, not index positions
shuffled_df = df.loc[[shuffled indices]]
df.loc[:] += shuffled_df # Simply doubles the values of df

# Let's say you have a 2-level MultiIndex.
# First level: ind1, ind2, ...
# Second level: ind1.1, ind1.2, ..., ind2.1, ind2.2 ...
df.loc[ind1] # Returns a DataFrame with a single index. Slices into rows corresponding to ind1, so the single index is ind1.1, ind1.2, ...
df.loc[(ind1, ind1.1)] # Returns a Series
df.loc[[(ind1, ind1.1)]] # Returns a DataFrame
df.loc[(ind1, ind1.1), col] # Returns element
df.loc[(ind1, ind1.1):ind3] # Slice from index tuple to single label
df.loc[(ind1, ind1.1):(ind3, ind3.2)] # Slices from index tuple to index tuple
```

## Index-based selection with iloc

Rows/cols may be
* An integer
* A list or array of integers
* A slice object of ints
* A boolean array
* A callable function with one argument (the calling Series or DataFrame) that returns a valid output for indexing (one of the above)
* A tuple of row and column indexes. The tuple elements consist of one of the above inputs.
```python
# df.iloc[rows, cols]

df.iloc[0] # Returns row as Series
df.iloc[[0]] # Returns row as DataFrame
df.iloc[[0, 1]] # Returns multiple rows as DataFrame
df.iloc[:3]
df.iloc[[True, False, True]] # Boolean mask must be same length as number of rows
df.iloc[lambda df: df.index % 2 == 0] # This only works if index is integer-based
df.iloc[0, 1] # Returns element
df.iloc[[0, 1], [0, 1]]
df.iloc[:10, :10]
df.iloc[:, [True, False, False, ...]] # Boolean mask must be same length as number of columns
```

## Filtering with query

`df.query(string expression representing condition)`

String expression example: `'(col1 > @outside_var) and (col2 < 5) and (col3 == "ex")'`
* Filters on columns (like SQL WHERE)
* Use `@outside_var` to access namespace variables
* Use double quotes for string literals

## Advanced indexing
Read more here: https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-advanced-hierarchical

If you have a DataFrame or Series with a MultiIndex, you can reset it with `df.reset_index()`.

## Setting index using columns

Use `df.set_index()` when you want to create a new index based on a column in `df`.

## All index modifications

set_index
reset_index

# Summary functions

* `df/series.describe()` - type aware, e.g. behavior is different based on data type like `int`, `str`, etc.
* `size()`

Numerical summaries. `df` method returns Series (val per column), `series` method returns element.
* `df/series.info()`
* `df/series.mean()`
* `df/series.min()`
* `df/series.max()`
* `df/series.median()`
* `df/series.std()`
* `df/series.var()`
* `df/series.count()`
* `df/series.sum()`
* `df/series.quantile([list of quantiles as floats])`
* `df/series.agg([list of summary functions])` - `df` returns DataFrame (vals vs. columns), `series` returns Series (vals per function).
* `df/series.agg(dict{key = column name, value = list of summary functions})`

Categorical/numerical summaries:
* `series.unique()` - unique values
* `series.nunique()` - number of unique values
* `series.value_counts(normalize=True/False)` - combo of above
* `df.value_counts()` - if multiple columns, then returns a MultiIndex Series

# Advanced column methods (rank, shift, cumsum)

`df/series.rank()` - method arg "dense", "first"
`df/series.shift()` - fill_value
`df/series.cumsum()`
`cummax()`
`cummin()`
`cumprod()`

## Rolling methods

* `df/series.rolling(window=n)` - returns Rolling object
* `df/series.rolling(window=n).mean()` - returns rolling mean with window size n

## Clip

* `df/series.clip(minval, maxval)` - clip values

# Creating new columns in DataFrame

* `df[new_col] = a Series or iterable, which can be constructed via an operation on an existing column in df` - modifies in place
* `df.assign(new_col = a Series or iterable)` - returns new object, can be used in a method chain

# Mapping

`series.map(elementwise_func)` - `elementwise_func` expects a single value from a Series, and `map` applies it to each element in `series`; returns a new Series with the transformed elements.
```python
def elementwise_func(x):
    return x*2

series2 = series.map(elementwise_func)
series3 = series.map(lambda x: x*3)
```
`df.apply(row_or_columnwise_func, axis="index" or "columns")` - `row_or_columnwise_func` expects a single row or column from a DataFrame, and `apply` applies the function to each row or column in the DataFrame; returns a new DataFrame.
```python
def rowwise_func(row):
    row.col1 = row.col1 + row.col2
    row.new_col = row.col1*2
    return row

# axis is "columns" for a rowwise function
df2 = df.apply(rowwise_func, axis="columns")
```

Built-in mapping operations:
```python
reviews.points - reviews.points.mean() # Subtracts mean from points column
reviews.country + " - " + reviews.region_1 # Mapping operation on Series of equal length

# All standard Python operators work in this manner, like >, <, ==, etc.
```

# Grouping and sorting

`df.groupby([columns to group by])` - slices `df` into groups on the unique value in a column (or the unique combinations of columns).

If `groupby` is called with multiple columns, then the result of the aggregate function will have MultiIndex, otherwise Index.

* `df.groupby([col(s)])` - returns DataFrameGroupBy object
* `df.groupby([col(s)])[[col(s)]]` - also returns DataFrameGroupBy object for specific columns (subsetting)
* `df.groupby([col(s)]).col` - returns SeriesGroupBy object

You can apply aggregate (summary) functions (including `agg`) to these GroupBy objects (no different from how you use aggregate functions with DataFrames and Series). With grouping, you get summaries for each group.
* `SeriesGroupBy.agg([funcs])` - returns DataFrame. Groups vs. func values.
* `DataFrameGroupBy.agg([funcs])` - returns DataFrame with MultiIndex columns. Index levels: column -> func values. MultiIndex is a list of tuples, so you can flatten via list comprehension, e.g. `df_agg.columns = ['_'.join(c) for c in df_agg.columns]`

Equivalent:
* `df.col.value_counts()`
* `df.groupby([col]).col.count()`
* `df.groupby([col]).size()`

Sorting:
* `df.sort_values(by=[col(s)], axis="index" or "columns", ascending=[boolean(s)])` - can also be applied to levels in hierarchical indexes and columns
* `df.sort_index()`
* `df.reset_index()` can be used to reset the index after sorting by column values

# Data types and missing values

* `df.dtypes`
* `series.dtype`
* For columns with `str` entries, the dtype is object
* `series.astype(type)` - convert to type
* `index.dtype` - index has dtype

Entries with missing values are given the value NaN, which is float64 type. To filter by NaN entries, use
* `pd.isnull(series)` or `pd.isna(series)`
* `pd.notnull(series)` or `pd.notna(series)`
* `df/series.isna()` or `df/series.isnull()`
* `df/series.notna()` or `df/series.notnull()`

To replace missing values, use 
* `df/series.dropna(subset=[col(s)])` - drop rows with NaN. Use subset to drop based on column subset.
* `df/series.fillna(replacement_value)` - replace all NaNs with replacement_value
* `series.bfill()` - backfill NaNs with next valid observation
* `series.replace(old_val, new_val)` to replace non-null values

# Renaming and combining

```python
df.rename(columns={"col1": "new_col1", "col2": "new_col2"})
df.rename(index={"index1": "new_index1", "index2", "new_index2"})
```

You can name the axes. 
```python
# Access names of axes - default is None
df.index.name
df.columns.name

# Give names to axes
df.rename_axis("row_axis_name", axis="rows")
df.rename_axis("column_axis_name", axis="columns")
```

`pd.concat([df1, df2, ...], axis=0 or 1)` - if `axis=0`, stack vertically (join DataFrames/Series based on same columns); if `axis=1`, stack horizontally (join based on same index). The DataFrames need to have the same columns/index. Generally `axis=1` is not used because you could stack DataFrames with the same column names (use `join` or `merge`). 

However, if you do stack horizontally and need to remove duplicate columns, you can either
* `df = df.loc[:, ~df.columns.duplicated()].copy()`
* `df = pd.concate([df, df], axis=1).set_flags(allows_duplicate_labels=False)`

`df1.join(df2, lsuffix="left", rsuffix="right")` to join DataFrames with the same index. Can also join based on columns.

`df1.merge(df2, how)` - like SQL join. `how` can be left, right, inner, outer.
* `validate` option: check if merge keys are unique. 
    * 1:1
    * 1:m
    * m:1
    * m:m

* `pd.merge(df1, df2, how, on=[col(s)], suffixes=("_1", "_2"))`
* `pd.merge(df1, df2, left_on=[col(s)], right_on=[col(s)])` - if DataFrames do not have the same column names