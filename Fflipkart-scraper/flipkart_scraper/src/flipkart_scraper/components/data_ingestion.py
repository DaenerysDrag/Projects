import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import re
from flipkart_scraper.config import (
    RETRIES, BACKOFF_FACTOR, MAX_PAGES, REQUEST_TIMEOUT, USER_AGENT
)


class FlipkartScraper:
    def __init__(self, brand):
        self.brand = brand
        self.base_url = "https://www.flipkart.com"
        self.search_url = f"{self.base_url}/search?q={self.brand}+washing+machine"
        self.retries = RETRIES
        self.backoff_factor = BACKOFF_FACTOR
        self.max_pages = MAX_PAGES
        self.timeout = REQUEST_TIMEOUT

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _get_page(self, url):
        """Fetch a URL with retry + exponential backoff. Returns raw bytes or None."""
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    url,
                    headers={'User-Agent': USER_AGENT},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                time.sleep(random.uniform(1, 3))
                return response.content
            except requests.exceptions.RequestException as e:
                logging.warning(
                    f"Request failed for {url} (attempt {attempt + 1}/{self.retries}): {e}"
                )
                if attempt < self.retries - 1:
                    time.sleep(self.backoff_factor * (2 ** attempt))
                else:
                    logging.error(f"All retries exhausted for {url}.")
        return None

    def _extract_product(self, card):
        """Extract all fields from a single product card element."""
        # Product name
        name_el = card.find('div', {'class': 'RG5Slk'})
        name = name_el.get_text(strip=True) if name_el else None

        # Product URL
        link_el = card.find('a', {'class': 'k7wcnx'})
        url = (self.base_url + link_el['href']) if link_el else None

        # Selling price (e.g. "₹17,490")
        price_el = card.find('div', {'class': 'DeU9vF'})
        price = price_el.get_text(strip=True) if price_el else None

        # Rating (e.g. "4.3")
        rating_el = card.find('span', {'class': 'CjyrHS'})
        rating = rating_el.get_text(strip=True) if rating_el else None

        # Reviews (e.g. "1,14,958 Ratings&7,235 Reviews")
        reviews_el = card.find('span', {'class': 'PvbNMB'})
        reviews = reviews_el.get_text(strip=True) if reviews_el else None

        # Model — extract text in parentheses from name, e.g. "(WW70T4S21VX)"
        model = None
        if name:
            match = re.search(r'\(([^)]+)\)', name)
            if match:
                model = match.group(1)

        return name, price, rating, reviews, url, model

    def _parse_page(self, content):
        """Parse all product cards from page HTML and return a list of dicts."""
        soup = BeautifulSoup(content, 'html.parser')

        product_cards = soup.find_all('div', {'class': 'nZIRY7'})

        if not product_cards:
            logging.warning(
                "No product cards matched class 'nZIRY7' — "
                "Flipkart may have updated its HTML structure."
            )

        products = []
        for card in product_cards:
            name, price, rating, reviews, url, model = self._extract_product(card)
            if name and price:
                products.append({
                    'Brand': self.brand,
                    'Product Name': name,
                    'Model': model,
                    'Price': price,
                    'Rating': rating,
                    'Number of Reviews': reviews,
                    'URL': url,
                })

        return products

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def scrape(self):
        """
        Scrape search results for the brand across up to MAX_PAGES pages.
        Stops early if a page returns no products.
        """
        all_products = []

        for page in range(1, self.max_pages + 1):
            url = f"{self.search_url}&page={page}"
            logging.info(f"Scraping page {page}/{self.max_pages} for {self.brand}...")

            content = self._get_page(url)
            if content is None:
                logging.warning(f"Skipping page {page} for {self.brand} — fetch failed.")
                break

            products = self._parse_page(content)
            if not products:
                logging.warning(
                    f"No products on page {page} for {self.brand}. Stopping pagination."
                )
                break

            logging.info(f"Found {len(products)} products on page {page} for {self.brand}.")
            all_products.extend(products)

        return all_products
