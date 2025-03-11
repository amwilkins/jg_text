# amw - 2025-02-16
# Scrape for text of articles
# Creates article_links.json and articles.json

import json
import re
import requests
import os

from bs4 import BeautifulSoup

import clean

URL = "https://jaypgreene.com/"
page_url = "page/{}/"
ARTICLE_LINKS = "outputs/article_links.json"
ARTICLES = "outputs/articles.json"


# extract links from page
def parse_main(page):
    page_url = URL + page
    print(f"extracting {page_url}")
    r = requests.get(page_url)
    soup = BeautifulSoup(r.content, "lxml")

    article_links = [
        i["href"].split("#")[0].split("?")[0]
        for i in soup.find_all(
            "a", attrs={"href": re.compile("^https://jaypgreene.com/2.+")}
        )
    ]
    return article_links


def scrape_main():
    # parse pages for links
    all_article_links = []
    for i in range(0, 350):
        all_article_links.extend(parse_main(page_url.format(i)))

    article_links = list(set(all_article_links))

    with open(ARTICLE_LINKS, "w") as file:
        json.dump(
            [{"url": url} for url in article_links],
            file,
            indent=4,
        )


# parse a single page and extract <p> tags
def parse_page(href):
    page_info = {}
    r = requests.get(href)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content.decode("utf-8", "ignore"), "lxml")
        match = re.search(r"https://jaypgreene.com/(\d{4}/\d{2}/\d{2})/.+", href)
        # match date
        if match:
            date_str = match.group(1)
            date_str = date_str.replace("/", "-")
        else:
            date_str = None

        # match title
        title_match = re.search(r"https://jaypgreene.com/2.+/(.+)/?", href)
        if title_match:
            title = title_match.group(1)
        else:
            title = None
        paragraphs = soup.find("div", {"class": "entry"}).find_all("p")[:-1]
        text_list = []
        for i in paragraphs:
            text_list.append(i.text)
        text = " ".join(text_list)
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace("\xa0", " ")
        page_info = {
            "url": href,
            "date": date_str,
            "title": title,
            "text": text,
        }

        return page_info
    else:
        print(f"Failed to retrieve {href}")
        return []


# Load links and parse all pages
def scrape_pages():
    # load in links
    with open(ARTICLE_LINKS, "r") as file:
        article_links = json.load(file)

    with open(ARTICLES, "w", encoding="utf-8") as output_file:
        articles = []
        n_links = len(article_links)
        count = 0
        for link in article_links:
            try:
                article_info = parse_page(link["url"])
                if article_info:
                    articles.append((article_info))
                print(f"Article {count}/{n_links}")
            except:
                pass
            count = count + 1
        json.dump(articles, output_file, indent=4)

    if len(article_links) == n_links:
        os.remove(ARTICLE_LINKS)


if __name__ == "__main__":
    scrape_main()
    scrape_pages()
    clean.clean_articles(ARTICLES)
