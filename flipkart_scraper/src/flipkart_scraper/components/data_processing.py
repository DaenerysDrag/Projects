import pandas as pd

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data)

    def process(self):
        """
        Cleans and normalizes the scraped data.
        """
        if self.df.empty:
            return self.df

        # Define the expected columns
        columns = ['Brand', 'Product Name', 'Model', 'Price', 'Rating', 'Number of Reviews', 'URL']
        for col in columns:
            if col not in self.df.columns:
                self.df[col] = None

        # Reorder columns to a consistent format
        self.df = self.df[columns]

        # Clean Price column
        self.df['Price'] = self.df['Price'].str.replace('[₹,]', '', regex=True).astype(float)

        # Clean Rating column
        self.df['Rating'] = pd.to_numeric(self.df['Rating'], errors='coerce')

        # Clean Number of Reviews column
        self.df['Number of Reviews'] = self.df['Number of Reviews'].str.replace(',', '').str.extract('(\d+)').astype(float)

        # Add a timestamp
        self.df['Timestamp'] = pd.to_datetime('now')

        return self.df
