### This script is for looking at niche genres. I want to consolidate the genres into fewer categories.
### There are 983 unique genres.
### Alternatively, every book seems to be categorized into multiple genres, so maybe I don't need to consolidate.

import numpy as np
import pandas as pd
from itertools import chain
import re
import json

""" Part 1 """

# df = pd.read_csv("books_1.Best_Books_Ever.csv")

# cleanup = re.compile(r"\[|\]|'")
# df['genres'] = df['genres'].apply(lambda x: re.sub(cleanup, "", x))
# df['genres_list'] = df['genres'].apply(lambda x: re.split(r",\s*", x))
# genres_total = list(chain.from_iterable(df['genres_list']))
# genres_set = list(set(genres_total))
# # print(genres_set)
# print(f"Number of unique genres: {len(genres_set)}")

# total_entries = len(df)
# genres_count = []
# for genre in genres_set:
#     # print(genre)
#     n = len(np.where(df["genres"].apply(lambda x: re.search(genre, x)))[0])
#     print(f"{genre}: {n}")
#     genres_count.append(n/total_entries)
#     # raise Exception("stop here")

# genres_count_dict = {"genres": genres_set, "percentage": genres_count}
# with open("genres_count.json", "w") as f:
#     json.dump(genres_count_dict, f)

""" Part 2 """

# with open("genres_count.json") as f:
#     genres_count = json.load(f)

# df = pd.DataFrame.from_dict(genres_count)
# df = df.sort_values(by="percentage", ascending=False)
# df.to_csv("genres_percentage_of_entries.csv")

""" Part 3 """

df = pd.read_csv("books_1.Best_Books_Ever.csv")

cleanup = re.compile(r"\[|\]|'")
df['genres'] = df['genres'].apply(lambda x: re.sub(cleanup, "", x))
# df['genres_list'] = df['genres'].apply(lambda x: re.split(r",\s*", x))

# print(df["genres"].apply(lambda x: re.search("Roman", x)))
idxs = np.where(df["genres"].apply(lambda x: re.search(r"\bRoman\b", x)))

df = df.iloc[idxs]
df = df.sort_values(by="numRatings", ascending=False)
print(df.iloc[0]["genres"])
print(df.head(5))