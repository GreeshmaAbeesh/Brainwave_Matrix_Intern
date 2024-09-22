import requests
from bs4 import BeautifulSoup
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


# Function to scrape tweets from a public source (e.g., Google)
def scrape_tweets():
    url = "https://www.google.com/search?q=CoronaOutbreak+site:twitter.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = []
    for result in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        tweets.append(result.get_text())
    return tweets


# Clean and process the tweets
def process_tweets(tweets):
    text = " ".join(tweets)
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")
    final_words = [word for word in tokenized_words if word not in stopwords.words('english')]
    return cleaned_text, final_words


# Perform sentiment analysis using VADER
def sentiment_analyse(sentiment_text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(sentiment_text)

    neg = score['neg']
    pos = score['pos']
    neu = score['neu']

    # Determine the overall sentiment based on the highest score
    if pos > neg and pos > neu:
        print("Positive Sentiment")
    elif neg > pos and neg > neu:
        print("Negative Sentiment")
    else:
        print("Neutral Vibe")

    # Also print detailed scores
    print(score)
    return score

# Visualize the sentiment analysis scores
def plot_sentiments(scores):
    labels = ['Positive', 'Negative', 'Neutral', 'Compound']
    values = [scores['pos'], scores['neg'], scores['neu'], scores['compound']]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['green', 'red', 'blue', 'purple'])
    plt.title('Sentiment Analysis Scores')
    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.show()


# Main function
if __name__ == "__main__":
    # Scrape tweets
    tweets = scrape_tweets()

    # Process the tweets (remove punctuation, stopwords, etc.)
    cleaned_text, final_words = process_tweets(tweets)

    # Perform sentiment analysis using VADER
    sentiment_scores = sentiment_analyse(cleaned_text)

    # Plot the sentiment analysis results
    plot_sentiments(sentiment_scores)
