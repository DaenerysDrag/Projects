import pandas as pd
import logging


class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data)

    def process(self):
        """
        Cleans and normalises the scraped data.
        Returns an empty DataFrame if there is nothing to process.
        """
        if self.df.empty:
            return self.df

        # Ensure every expected column exists (fills missing ones with None)
        columns = ['Brand', 'Product Name', 'Model', 'Price', 'Rating', 'Number of Reviews', 'URL']
        for col in columns:
            if col not in self.df.columns:
                self.df[col] = None

        self.df = self.df[columns]

        # --- Price ---
        # Convert to string first so .str methods are safe on None/NaN values,
        # then strip the rupee symbol and commas before casting to float.
        self.df['Price'] = (
            self.df['Price']
            .astype(str)
            .str.replace('[₹,]', '', regex=True)
            .str.strip()
        )
        self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')

        # --- Rating ---
        self.df['Rating'] = pd.to_numeric(self.df['Rating'], errors='coerce')

        # --- Number of Reviews ---
        # Safe string coercion before .str operations, then extract the first
        # integer found (handles formats like "1,234 Ratings" or "1234 Reviews").
        self.df['Number of Reviews'] = (
            self.df['Number of Reviews']
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.extract(r'(\d+)', expand=False)
        )
        self.df['Number of Reviews'] = pd.to_numeric(
            self.df['Number of Reviews'], errors='coerce'
        )

        # --- Timestamp ---
        self.df['Timestamp'] = pd.to_datetime('now')

        # --- Validation ---
        # Drop rows where Price is missing or zero — they are unusable.
        before = len(self.df)
        self.df = self.df[self.df['Price'].notna() & (self.df['Price'] > 0)]
        dropped = before - len(self.df)
        if dropped:
            logging.warning(f"Dropped {dropped} row(s) with missing or zero Price.")

        return self.df
