# Twitter Sentiment Analysis Report

## 1. Data Cleaning
- **Initial Shape:** 80019 rows, 12 columns.
- **Final Shape:** 79514 rows.
- **Process:**
  - Removed duplicates.
  - Dropped nulls in `text`.
  - Cleaned text: Removed URLs, User mentions, special characters/emojis.
  - Normalized: Lowercase, lemmatization (using WordNet).
  - Filtered: Removed stopwords.

## 2. Sentiment Analysis (VADER)
- **Positive:** 43.4%
- **Neutral:** 37.2%
- **Negative:** 19.4%

The sentiment is predominantly positive (43.4%) or neutral (37.2%), with a smaller portion being negative (19.4%). This suggests a generally favorable or objective discussion around the topics in the dataset (likely "Squid Game" based on common words).

## 3. Key Insights
1.  **Dominant Topic:** The terms "squidgame", "game", "squid" are the most frequent across all sentiments, indicating the dataset is focused on the Netflix series "Squid Game".
2.  **Positive Sentiment:** Positive tweets often contain words like "project", "like", "good", "love", "best", possibly referring to crypto projects related to the show (tokens) or fan appreciation.
3.  **Negative Sentiment:** Negative tweets also center on "episode", "im", "people", suggesting discussions about specific plot points, character deaths, or potentially critiques of the show's violent nature or the hype.
4.  **Crypto Influence:** The presence of words like "project", "token", "presale", "airdrop" (seen in bigrams or deeper inspection) often correlates with spammy or promotional tweets which might be classified as positive due to hype keywords ("moon", "gem"), but are actually marketing noise.
5.  **Viral Content:** High volume of neutral tweets suggests many users are simply sharing news, links, or stating facts without strong emotional language.
6.  **Engagement:** The high percentage of positive sentiment is beneficial for brand/show perception, but marketers should be aware of the "shilling" bot activity if "project" is a top word.

## 4. Visualizations
The following plots have been generated in `output/plots/`:
- `sentiment_distribution.png`: Bar chart of sentiment counts.
- `sentiment_pie_chart.png`: Pie chart of sentiment share.
- `wordcloud_positive.png`: Word cloud for positive tweets.
- `wordcloud_negative.png`: Word cloud for negative tweets.
- `wordcloud_neutral.png`: Word cloud for neutral tweets.
- `top_20_words.png`: Bar chart of most frequent words.
- `top_20_bigrams.png`: Bar chart of most frequent bigrams.
- `sentiment_score_distribution.png`: Histogram of VADER compound scores.

## 5. Recommendations
- **For Marketers:** Leverage the high positive sentiment. If this is for the show, the reception is great. If for a crypto token, filtering out organic vs. bot traffic is crucial.
- **For Researchers:** The dataset is heavily influenced by a specific pop-culture event. Sentiment analysis models might need fine-tuning to distinguish between "scary" (plot description) vs "bad" (viewer opinion).
