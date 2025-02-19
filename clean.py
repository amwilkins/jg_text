# amw - 2025-02-17
# Cleaning and tokenizing text

import json
import os
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

ARTICLE_LINKS = "outputs/article_links.json"
ARTICLES = "outputs/articles.json"

with open(ARTICLES) as file:
    articles = json.load(file)
n_articles = len(articles)


# fixing encoding errors
def clean_text(text_list):
    text = " ".join(text_list)
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = text.replace("\xa0", " ")
    return text


stop_words = set(stopwords.words("english"))
count = 0
for i in articles:
    if i["paragraphs"]:
        i["text"] = clean_text(i["paragraphs"])
        del i["paragraphs"]

    i["tokens"] = [
        word
        for word in word_tokenize(i["text"])
        if word.isalnum() and word.lower() not in stop_words
    ]

    i["len"] = len(i["tokens"])

    print(f"Processed: {count}", end="\r")
    count = count + 1

if len(articles) == n_articles:
    with open("outputs/corpus.json", "w") as output_file:
        json.dump(articles, output_file, indent=4)

    os.remove(ARTICLES)
