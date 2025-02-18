from openai import OpenAI
import os
import re
import numpy as np
import pandas as pd
import argparse
import json

def generate_synthetic_queries(client: OpenAI, category: str, examples: list[str], num_samples: int=20):
    prompt = f"""
    You are an AI assistant helping to generate diverse user queries for an intent classifier.
    The intent classifier will be the first block in a book recommendation chatbot application.
    The main genres are [Fiction,Adult,Romance,Fantasy,Young Adult,Contemporary,Literature,Novels,Historical,Nonfiction,Science,Mystery,Historical Fiction,Classics,Science Fiction,Adventure,Childrens,Thriller,Humor,History,Crime,Biography,Horror,Teen,Philosophy,Memoir,Short Stories,Religion].
    The goal is to create natural-sounding, varied queries for the following category: **{category}**.
    
    Here are some real user examples for this category:
    {examples}

    Please generate {num_samples} new user queries that fit this category. 
    Ensure they:
    - Vary in phrasing and structure.
    - Include short, medium, and long queries.
    - Are conversational and natural.
    - Avoid overlapping too much with the provided examples.

    Output each query on a new line, and only give me the queries, no other text.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" for cost efficiency
        messages=[{"role": "system", "content": "You generate diverse user queries for intent classification."},
                  {"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.7  # Adjust for more/less randomness
        # temperature=1
    )

    return response.choices[0].message.content

def apply_regex(samples: str):
    split_samples = re.split(r"\n", samples)
    # print(split_samples)

    # Remove list numbering if needed
    pattern = re.compile(r"^\d+.\s*")
    split_samples = [pattern.sub("", sample) for sample in split_samples]
    pattern = re.compile(r"^-\s*")
    split_samples = [pattern.sub("", sample) for sample in split_samples]
    # print(split_samples)

    return split_samples  

def save_to_csv(samples: list[str], Label: str, Notes: str, Category: str, csv_file: str):
    n = len(samples)
    sample_dict = {
        "Query": samples,
        "Label": np.ones(n)*Label,
        "Notes": [Notes]*n,
        "Category": [Category]*n,
    }

    sample_df = pd.DataFrame.from_dict(sample_dict)
    sample_df = sample_df.loc[sample_df["Query"].apply(lambda x: len(x)>0)] # remove empty strings

    if os.path.isfile(csv_file):
        sample_df.to_csv(csv_file, mode="a", index=False, header=False)
    else:
        sample_df.to_csv(csv_file, mode="w", index=False, header=True)

if __name__ == "__main__":
    """
    Recommended usage for synchronous call to OpenAI API: python3 generate_synthetic_samples.py -f intent_classifier_samples.csv -l 0
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="CSV file to store synthetic samples")
    parser.add_argument("-l", "--label", type=int, help="Label to generate")
    # parser.add_argument("-b", "--batch", action="store_true", help="Use OpenAI batch API")
    parser.add_argument("-r", "--real", action="store_true", help="Provide only human-generated samples to chat completion endpoint")
    parser.add_argument("-n", "--number", type=int, default=20, help="Number of synthetic samples to generate")
    args = parser.parse_args()

    df = pd.read_csv(args.file)
    df = df.loc[df["Label"] == args.label]
    if args.real:
        df = df.loc[df["Notes"] == "Real"]
    category = df.iloc[0]["Category"]
    examples = df["Query"].to_list()
    # print(category)
    # print(examples)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    synth_samples = generate_synthetic_queries(client, category, examples, num_samples=args.number)
    synth_samples2 = apply_regex(synth_samples)
    save_to_csv(synth_samples2, args.label, "Synthetic", category, args.file)