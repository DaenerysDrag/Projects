from flipkart_scraper.components.data_ingestion import FlipkartScraper
from flipkart_scraper.components.data_processing import DataProcessor
from flipkart_scraper.components.data_storage import ExcelStorage
from flipkart_scraper.utils.common import setup_logging
from flipkart_scraper.config import BRANDS, EXCEL_FILENAME
import logging

def main():
    setup_logging()

    for brand in BRANDS:
        try:
            logging.info(f"Scraping data for {brand}...")
            scraper = FlipkartScraper(brand)
            raw_data = scraper.scrape()

            if raw_data:
                logging.info(f"Processing data for {brand}...")
                processor = DataProcessor(raw_data)
                processed_data = processor.process()

                logging.info(f"Storing data for {brand}...")
                storage = ExcelStorage(filename=EXCEL_FILENAME)
                storage.store(processed_data, brand)
                logging.info(f"Data for {brand} stored successfully.")
            else:
                logging.warning(f"No data scraped for {brand}.")

        except Exception as e:
            logging.error(f"An error occurred while processing {brand}: {e}")

if __name__ == "__main__":
    main()
