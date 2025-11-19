import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import logging
import re
from flipkart_scraper.config import RETRIES, BACKOFF_FACTOR

class FlipkartScraper:
    def __init__(self, brand):
        self.brand = brand
        self.base_url = "https://www.flipkart.com"
        self.search_url = f"{self.base_url}/search?q={self.brand}+washing+machine"
        self.user_agent = UserAgent()
        self.retries = RETRIES
        self.backoff_factor = BACKOFF_FACTOR

    def scrape(self):
        """
        Scrapes data for the specified brand with retry logic.
        """
        headers = {'User-Agent': self.user_agent.random}

        for i in range(self.retries):
            try:
                response = requests.get(self.search_url, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes

                time.sleep(random.uniform(1, 3))

                soup = BeautifulSoup(response.content, 'html.parser')
                products = []

                # Updated selectors for Flipkart's current structure
                for product in soup.find_all('div', {'class': 'cPHDOP'}):
                    name_element = product.find('div', {'class': 'KzDlHZ'})
                    price_element = product.find('div', {'class': 'Nx9bqj CxhGGd'})
                    rating_element = product.find('div', {'class': 'XQDdHH'})
                    reviews_element = product.find('span', {'class': 'Wphh3N'})
                    url_element = product.find('a', {'class': 'CGtC98'})

                    name = name_element.text.strip() if name_element else None
                    price = price_element.text.strip() if price_element else None
                    rating = rating_element.text.strip() if rating_element else None
                    reviews = reviews_element.text.strip() if reviews_element else None
                    url = self.base_url + url_element['href'] if url_element else None

                    # Extract model from the name
                    model = None
                    if name:
                        # Look for a pattern like (ABC1234)
                        match = re.search(r'\((.*?)\)', name)
                        if match:
                            model = match.group(1)

                    if name and price:
                        products.append({
                            'Brand': self.brand,
                            'Product Name': name,
                            'Model': model,
                            'Price': price,
                            'Rating': rating,
                            'Number of Reviews': reviews,
                            'URL': url
                        })

                return products

            except requests.exceptions.RequestException as e:
                logging.warning(f"Request failed for {self.brand} (attempt {i+1}/{self.retries}): {e}")
                if i < self.retries - 1:
                    sleep_time = self.backoff_factor * (2 ** i)
                    time.sleep(sleep_time)
                else:
                    logging.error(f"All retries failed for {self.brand}.")
                    return []
        return []
