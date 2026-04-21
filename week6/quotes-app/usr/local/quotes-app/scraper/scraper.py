import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


os.makedirs("raw_data", exist_ok=True)
os.makedirs("processed_data", exist_ok=True)

def get_page(page):
    url = f"https://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def extract_raw_quotes(soup):
    raw_quotes = []

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        raw_quotes.append({
            "quote": q.find("span", class_="text").text,
            "author": q.find("small", class_="author").text,
            "tags": [t.text for t in q.find_all("a", class_="tag")]
        })

    return raw_quotes


def scrape_all_raw():
    page = 1
    all_raw = []

    while True:
        print(f"Scraping RAW page {page}...")

        soup = get_page(page)
        quotes = extract_raw_quotes(soup)

        if not quotes:
            break

        all_raw.extend(quotes)
        page += 1

    return all_raw


def save_raw_json(data):
    with open("raw_data/quotes_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



def load_raw_data():
    with open("raw_data/quotes_raw.json", "r", encoding="utf-8") as f:
        return json.load(f)


def clean_data(raw_data):
    cleaned = []

    for item in raw_data:
        cleaned.append({
            "quote": item["quote"].strip(),
            "author": item["author"].strip(),
            "tags": item["tags"],
            "tags_count": len(item["tags"]) 
        })

    return cleaned


def save_processed_json(data):
    with open("processed_data/quotes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_processed_csv(data):
    df = pd.DataFrame(data)

    df["tags"] = df["tags"].apply(lambda x: ", ".join(x))

    df.to_csv("processed_data/quotes.csv", index=False, encoding="utf-8")


