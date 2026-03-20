# List of brands to scrape
BRANDS = ["Samsung", "LG", "Whirlpool", "Haier"]

# Excel file settings
EXCEL_FILENAME = 'Flipkart_WashingMachines.xlsx'

# Scraper settings
RETRIES = 3
BACKOFF_FACTOR = 0.5
MAX_PAGES = 3          # Number of search result pages to scrape per brand
REQUEST_TIMEOUT = 15   # Seconds before a request is considered timed out

# User-Agent that consistently returns structured HTML from Flipkart
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.212 Safari/537.36"
)
