# amw - 2025-02-17
# Cleaning and tokenizing text

import json
import sys

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

CORPUS = "outputs/corpus.json"
ARTICLES = "outputs/articles.json"


# fixing encoding errors
def clean_text(text):
    # text = " ".join(text)
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = text.replace("\xa0", " ")
    text = text.replace("\u0394 Create a free website or blog at WordPress.com.", " ")
    text = text.replace("Blog at WordPress.com.", " ")
    text = text.split("This entry was posted on ")[0]
    return text


def clean_articles(article_json):

    with open(article_json) as file:
        articles = json.load(file)
    n_articles = len(articles)

    stop_words = set(stopwords.words("english"))
    count = 0
    excluded = 0
    cleaned_articles = []
    for i in articles:
        count = count + 1
        try:
            i["text"] = clean_text(i["text"])
        except Exception as e:
            print(f"ERROR cleaning article text: {e}")
            sys.exit(1)

        i["tokens"] = [
            word
            for word in word_tokenize(i["text"])
            if word.isalnum() and word.lower() not in stop_words
        ]

        i["len"] = len(i["tokens"])

        # remove articles with no text (usually these are pictures)
        if i["len"] < 5:
            excluded += 1
            n_articles -= 1
        else:
            cleaned_articles.append(i)

        if count % 10 == 0:
            print(f"Processed: {count}, excluded articles: {excluded}", end="\r")

    if len(cleaned_articles) == n_articles:
        with open(CORPUS, "w") as output_file:
            json.dump(cleaned_articles, output_file, indent=4)


if __name__ == "__main__":
    clean_articles(ARTICLES)
