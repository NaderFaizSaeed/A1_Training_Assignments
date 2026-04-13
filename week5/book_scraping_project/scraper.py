import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pandas as pd
import os
import shutil

#  Scraping
def scrape_books():
    base_url = "https://books.toscrape.com/catalogue/category/books_1/"
    current_page = 1
    raw_books = []

    os.makedirs("data/raw/raw_images", exist_ok=True)
    os.makedirs("data/processed/processed_data", exist_ok=True)
    os.makedirs("data/raw/raw_data", exist_ok=True)



    while current_page <= 3:  #  نقدر نغير العدد كما نريد على حسب الصفحات الموجودة في الموقع
        url = f"{base_url}page-{current_page}.html"

        response = requests.get(url)
        soup = bs(response.text, "html.parser")

        articles = soup.find_all("article", class_="product_pod")

        for book in articles:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.find("p", class_="star-rating")["class"][1]

            # الصورة
            img_src = book.find("img")["src"]
            img_url = urljoin("https://books.toscrape.com/", img_src)

            img_name = name.replace(":", "").replace("/", "") + ".jpg"
            img_path = os.path.join("data/raw/raw_images", img_name)

            try:
                img_content = requests.get(img_url).content
                with open(img_path, "wb") as img_file:
                    img_file.write(img_content)
            except:
                img_path = None

            raw_books.append({
                "name": name,
                "price": price,
                "rating": rating,
                "image_path": img_path
            })

        current_page += 1

    df = pd.DataFrame(raw_books)
    df.to_csv("data/raw/raw_data/raw_data_of_books.csv", index=False)

    return df


#  Cleaning
def clean_data(df):
    df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["rating"].map(rating_map)

    df["name"] = df["name"].astype("string")
    df["image_path"] = df["image_path"].astype("string")

    df.to_csv("data/processed/processed_data/cleaned_data_of_books.csv", index=False)

    return df


#  Organize CSV by Rating
def organize_csv(df):
    base_folder = "data/processed/ratings_data"

    for i in range(1, 6):
        folder_path = os.path.join(base_folder, f"{i}_stars")
        os.makedirs(folder_path, exist_ok=True)

        df_rating = df[df["rating"] == i]
        file_path = os.path.join(folder_path, "data.csv")

        df_rating.to_csv(file_path, index=False)


#  Organize Images by Rating
def organize_images(df):
    base_folder = "data/images_by_rating"

    for i in range(1, 6):
        os.makedirs(os.path.join(base_folder, f"{i}_stars"), exist_ok=True)

    for _, row in df.iterrows():
        image_path = row["image_path"]
        rating = row["rating"]

        if image_path and os.path.exists(image_path):
            file_name = os.path.basename(image_path)

            destination = os.path.join(
                base_folder,
                f"{rating}_stars",
                file_name
            )

            try:
                shutil.copy(image_path, destination)
            except:
                print(f"Error moving {file_name}")


#  Full Pipeline
def run_pipeline():
    print("Scraping...")
    raw_df = scrape_books()

    print("Cleaning...")
    clean_df = clean_data(raw_df)

    print("Organizing CSV...")
    organize_csv(clean_df)

    print("Organizing Images...")
    organize_images(clean_df)

    print("Done!")