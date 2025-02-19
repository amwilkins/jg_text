# amw - 2025-02-17
# Exploring articles
# Plotting with plotnine

import json
import pandas as pd

from plotnine import ggplot, aes, geom_point, labs, theme_minimal
from datetime import datetime

CORPUS = "outputs/corpus.json"

with open(CORPUS) as file:
    articles = json.load(file)

dates = []
lengths = []
for article in articles:
    date_str = article["date"]
    if date_str is not None:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        dates.append(date_obj)
        lengths.append(article["len"])


data = pd.DataFrame({"Date": dates, "Length of Tokens (len)": lengths})
plot = (
    ggplot(data, aes(x="Date", y="Length of Tokens (len)"))
    + geom_point()
    + labs(title="Token Lengths Over Time", x="Date", y="Length of Tokens (len)")
    + theme_minimal()
)
plot.save("outputs/token_count_time.png")
plot.show()
