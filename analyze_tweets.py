import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from textblob import TextBlob
import re
import os
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

# Configure plotting style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

class TweetAnalyzer:
    def __init__(self, filepath, output_dir="output"):
        self.filepath = filepath
        self.output_dir = output_dir
        self.plots_dir = os.path.join(output_dir, "plots")
        os.makedirs(self.plots_dir, exist_ok=True)
        self.df = None

        # Download NLTK resources
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        try:
            nltk.data.find('corpora/stopwords.zip')
        except LookupError:
            nltk.download('stopwords')

        try:
            nltk.data.find('corpora/wordnet.zip')
        except LookupError:
            nltk.download('wordnet')

        try:
            nltk.data.find('corpora/omw-1.4.zip')
        except LookupError:
            nltk.download('omw-1.4')

    def load_data(self):
        """Loads the dataset."""
        print(f"Loading data from {self.filepath}...")
        self.df = pd.read_csv(self.filepath)
        print(f"Data loaded. Shape: {self.df.shape}")
        return self.df.head()

    def clean_text(self, text):
        """Cleans the text by removing URLs, emojis, special characters, etc."""
        if not isinstance(text, str):
            return ""

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Remove user mentions @user
        text = re.sub(r'@\w+', '', text)

        # Remove hashtags (keeping the word) - optional, but user asked to remove special chars
        # text = re.sub(r'#', '', text)

        # Remove emojis (non-ASCII characters) - simple approach
        text = text.encode('ascii', 'ignore').decode('ascii')

        # Remove special characters and numbers, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        # Lowercase
        text = text.lower()

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        text = " ".join([word for word in text.split() if word not in stop_words])

        # Lemmatize (optional, but requested "lemmatize/stem")
        # stemmer = nltk.PorterStemmer()
        # text = " ".join([stemmer.stem(word) for word in text.split()])

        # Let's use WordNetLemmatizer for better results than stemming
        lemmatizer = nltk.WordNetLemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

        return text

    def preprocess_data(self):
        """Performs data cleaning."""
        print("Cleaning data...")
        initial_shape = self.df.shape

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Remove nulls in text column
        self.df.dropna(subset=['text'], inplace=True)

        # Apply text cleaning
        self.df['cleaned_text'] = self.df['text'].apply(self.clean_text)

        # Remove empty cleaned text rows
        self.df = self.df[self.df['cleaned_text'] != ""]

        print(f"Data cleaning complete. Shape before: {initial_shape}, After: {self.df.shape}")

        return self.df[['text', 'cleaned_text']].head()

    def analyze_sentiment(self):
        """Performs sentiment analysis using VADER."""
        print("Analyzing sentiment...")
        sia = SentimentIntensityAnalyzer()

        def get_sentiment(text):
            score = sia.polarity_scores(text)
            compound = score['compound']
            if compound >= 0.05:
                return 'Positive', compound
            elif compound <= -0.05:
                return 'Negative', compound
            else:
                return 'Neutral', compound

        self.df[['sentiment_label', 'sentiment_score']] = self.df['cleaned_text'].apply(
            lambda x: pd.Series(get_sentiment(x))
        )

        sentiment_counts = self.df['sentiment_label'].value_counts(normalize=True) * 100
        print("Sentiment distribution (%):")
        print(sentiment_counts)
        return sentiment_counts

    def generate_visualizations(self):
        """Generates required plots."""
        print("Generating visualizations...")

        # 1. Sentiment Distribution Bar Chart
        plt.figure(figsize=(8, 6))
        ax = sns.countplot(x='sentiment_label', data=self.df, palette='viridis', order=['Positive', 'Neutral', 'Negative'])
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        # Add percentage labels
        total = len(self.df)
        for p in ax.patches:
            percentage = '{:.1f}%'.format(100 * p.get_height()/total)
            x = p.get_x() + p.get_width() / 2 - 0.05
            y = p.get_height()
            ax.annotate(percentage, (x, y), ha='center', va='bottom')
        plt.savefig(os.path.join(self.plots_dir, 'sentiment_distribution.png'))
        plt.close()

        # 2. Pie Chart (Optional but good)
        plt.figure(figsize=(7, 7))
        self.df['sentiment_label'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#66b3ff', '#99ff99', '#ff9999'])
        plt.title('Sentiment Percentage')
        plt.ylabel('')
        plt.savefig(os.path.join(self.plots_dir, 'sentiment_pie_chart.png'))
        plt.close()

        # 3. Word Clouds
        for label in ['Positive', 'Negative', 'Neutral']:
            subset = self.df[self.df['sentiment_label'] == label]
            text = " ".join(subset['cleaned_text'].tolist())
            if not text:
                continue
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Word Cloud - {label}')
            plt.savefig(os.path.join(self.plots_dir, f'wordcloud_{label.lower()}.png'))
            plt.close()

        # 4. Top 20 Most Frequent Words
        all_words = " ".join(self.df['cleaned_text']).split()
        word_freq = Counter(all_words)
        common_words = word_freq.most_common(20)
        words_df = pd.DataFrame(common_words, columns=['Word', 'Count'])

        plt.figure(figsize=(12, 8))
        sns.barplot(x='Count', y='Word', data=words_df, palette='magma')
        plt.title('Top 20 Most Frequent Words')
        plt.savefig(os.path.join(self.plots_dir, 'top_20_words.png'))
        plt.close()

        # 5. Bigram Analysis
        def get_top_n_bigrams(corpus, n=None):
            vec = CountVectorizer(ngram_range=(2, 2)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:n]

        top_bigrams = get_top_n_bigrams(self.df['cleaned_text'], 20)
        bigram_df = pd.DataFrame(top_bigrams, columns=['Bigram', 'Count'])

        plt.figure(figsize=(12, 8))
        sns.barplot(x='Count', y='Bigram', data=bigram_df, palette='plasma')
        plt.title('Top 20 Bigrams')
        plt.savefig(os.path.join(self.plots_dir, 'top_20_bigrams.png'))
        plt.close()

        # 6. Sentiment Score Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['sentiment_score'], kde=True, bins=30)
        plt.title('Sentiment Score Distribution')
        plt.xlabel('VADER Compound Score')
        plt.savefig(os.path.join(self.plots_dir, 'sentiment_score_distribution.png'))
        plt.close()

    def generate_insights(self):
        """Generates textual insights."""
        total_tweets = len(self.df)
        sentiment_counts = self.df['sentiment_label'].value_counts()

        print("\n--- INSIGHTS ---")
        print(f"Total Tweets Analyzed: {total_tweets}")
        print("Sentiment Breakdown:")
        for label, count in sentiment_counts.items():
            print(f"  {label}: {count} ({count/total_tweets:.1%})")

        # Most common words per sentiment
        print("\nMost Common Words per Sentiment:")
        for label in ['Positive', 'Negative']: # Focus on polar sentiments
            subset = self.df[self.df['sentiment_label'] == label]
            words = " ".join(subset['cleaned_text']).split()
            common = Counter(words).most_common(5)
            print(f"  {label}: {', '.join([w[0] for w in common])}")

        print("\nSee 'output/plots' for visual analysis.")

    def run(self):
        self.load_data()
        self.preprocess_data()
        self.analyze_sentiment()
        self.generate_visualizations()
        self.generate_insights()

        # Export cleaned data (Saving only head to avoid sandbox file size limits)
        # In a real environment, you would save the full dataframe:
        # self.df.to_csv(os.path.join(self.output_dir, 'cleaned_tweets.csv'), index=False)

        sample_path = os.path.join(self.output_dir, 'cleaned_tweets_sample.csv')
        self.df.head(100).to_csv(sample_path, index=False)
        print(f"Cleaned data sample saved to {sample_path}")

if __name__ == "__main__":
    analyzer = TweetAnalyzer("/tmp/file_attachments/tweets_v8.csv/tweets_v8.csv")
    analyzer.run()
