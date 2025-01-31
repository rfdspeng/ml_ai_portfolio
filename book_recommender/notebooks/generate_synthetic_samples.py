from openai import OpenAI
import os
import re
import numpy as np
import pandas as pd

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

    Output each query on a new line.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-3.5-turbo" for cost efficiency
        messages=[{"role": "system", "content": "You generate diverse user queries for intent classification."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
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

    sample_df.to_csv(csv_file, mode="a", index=False, header=False)

csv_file = "intent_classifier_samples.csv"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

""" Label 0 """
# category = "Direct book queries that request by title, series, author, genre, rating, popularity, language"
# examples = ["Do you have Harry Potter?",
#             "Do you have the Broken Earth series?",
#             "Do you have All Quiet on the Western Front?",
#             "Do you have anything by Kazuo Ishiguro?",
#             "I'm looking for books by Celeste Ng.",
#             "What do you have in stock written by Madeline Miller?",
#             "I prefer nonfiction.",
#             "I love science fiction books.",
#             "Do you have a historical fiction section?",
#             "What are some classic books that everyone should read?",
#             "What are your most popular books?",
#             "What are your most beloved books?",
#             "What books do you have in French?",
#             "Do you have any Spanish-language books?",
#             "I'm looking for books in Italian.",
#             "I'm doing research for an essay, and I'm looking for best-selling history books about the American Civil War.",
#             "Do you have any popular young adult fantasy series?",
#             "Do you have any memoirs by French authors?",]

""" Label 1 """
# category = "Direct book queries that ask for a similar book"
# examples = ["I really liked Circe (by Madeline Miller). Do you have any books like Circe?"]
# label = 1
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 2 """
# category = "Ambiguous queries that will prompt the book recommender chatbot to ask for clarification or additional information"
# examples = [
#     "Good morning, I was wondering if you could help me.",
#     "Hello! I'm looking for a book.",
#     "Can you recommend something?",
#     "I'm in the mood for something light and funny."
# ]
# label = 2
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 3 """
# category = "Follow-up requests to previous queries"
# examples = [
#     "I've read all those fantasy series. Can you recommend any others?",
#     "Do you have any other suggestions for memoirs?",
#     "What about books similar to the thrillers you recommended?",
# ]
# label = 3
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 4 """
# category = "Conversation history queries that don't require database retrieval"
# examples = [
#     "Can you remind me what you've recommended so far?"
# ]
# label = 4
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 5 """
# category = "Irrelevant queries"
# examples = [
#     "Hello, what's the weather today?",
#     "Hello, how's it going?"
# ]
# label = 5
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 6 """
# category = "Negative intent queries"
# examples = [
#     "I don't need any recommendations right now.",
#     "No, thank you, I'm just browsing."
# ]
# label = 6
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 7 """
# category = "System queries about the book recommender application"
# examples = [
#     "How do your recommendations work?",
#     "What kind of backend application framework are you using?",
#     "Are you calling any APIs?",
#     "Do you use any ML models?"
# ]
# label = 7
# save_to_csv(examples, label, "Real", category, csv_file)
# synth_samples = generate_synthetic_queries(client, category, examples)
# print(synth_samples)
# synth_samples2 = apply_regex(synth_samples)
# save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)

""" Label 8 """
category = "Queries about the dataset that require SQL or pandas to answer"
examples = [
    "Do you have books in other languages?",
    "What are your top 10 most popular books?",
    "Which genre do you have the most books of?",
    "Which series has the most books?",
    "What are your most popular authors?"
]
label = 8
save_to_csv(examples, label, "Real", category, csv_file)
synth_samples = generate_synthetic_queries(client, category, examples)
print(synth_samples)
synth_samples2 = apply_regex(synth_samples)
save_to_csv(synth_samples2, label, "Synthetic", category, csv_file)