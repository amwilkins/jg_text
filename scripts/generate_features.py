# amw - 2025-02-17
# Exploring articles
# Plotting with plotnine

import argparse
import json
import re

# import pandas as pd
#
# from plotnine import ggplot, aes, geom_point, labs, theme_minimal
# from datetime import datetime

from nltk import PunktSentenceTokenizer, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

CORPUS = "outputs/corpus.json"


def create_features(article):
    pst = PunktSentenceTokenizer()
    sid = SentimentIntensityAnalyzer()
    # sentence count and length
    sentences = pst.tokenize(article["text"])
    article["n_sentences"] = len(sentences)
    article["len_sentences"] = [len(word_tokenize(i)) for i in sentences]
    article["avg_sentence_length"] = round(
        sum(article["len_sentences"]) / article["n_sentences"], 2
    )

    # sentiment per sentence
    article["sent_sentences"] = []
    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        article["sent_sentences"].append(ss)
    article["avg_sent_sentences"] = {
        k: round(
            sum(d[k] for d in article["sent_sentences"]) / article["n_sentences"], 2
        )
        for k in article["sent_sentences"][0]
    }

    # flag guest posts
    if re.search("Guest Post by ", article["text"]):
        article["guest_flag"] = True
    else:
        article["guest_flag"] = False

    return article


def main():
    with open(CORPUS) as file:
        articles = json.load(file)

    data = []
    count = 0
    for article in articles:
        count += 1
        if count % 10 == 0:
            print(f"Processed: {count}", end="\r")
        data.append(create_features(article))

    with open(CORPUS, "w") as output_file:
        json.dump(data, output_file, indent=4)


# dates = []
# lengths = []
# for article in articles:
#     date_str = article["date"]
#     if date_str is not None:
#         date_obj = datetime.strptime(date_str, "%Y-%m-%d")
#         dates.append(date_obj)
#         lengths.append(article["len"])
#
#
# data = pd.DataFrame({"Date": dates, "Tokens": lengths})


# plot = (
#     ggplot(data, aes(x="Date", y="Length of Tokens (len)"))
#     + geom_point()
#     + labs(title="Token Lengths Over Time", x="Date", y="Length of Tokens (len)")
#     + theme_minimal()
# )
# plot.save("outputs/token_count_time.png")
# plot.show()

if __name__ == "__main":

    parser = argparse.ArgumentParser(description="A script with a test flag.")
    parser.add_argument("-t", "--test", action="store_true", help="Enable test mode")
    args = parser.parse_args()

    # if args.test:

    main()
