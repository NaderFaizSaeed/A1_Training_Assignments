from scraper.scraper import scrape_all_raw,save_raw_json,load_raw_data,clean_data,save_processed_json,save_processed_csv


def main():
    print(" Scraping data starts...")
    raw_data = scrape_all_raw()
    save_raw_json(raw_data)

    print(" RAW data saved")

    raw_loaded = load_raw_data()
    clean = clean_data(raw_loaded)

    save_processed_json(clean)
    save_processed_csv(clean)

    print(" Processed data saved")


if __name__ == "__main__":
    main()