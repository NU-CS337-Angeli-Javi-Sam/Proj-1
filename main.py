import os
import json
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Sample tweet data
tweets = [
    {'text': "JLo's dress! #eredcarpet #GoldenGlobes", 'user': {'screen_name': 'Dozaaa_xo', 'id': 557374298}},
    # Add more tweets here...
]

# Initialize NLTK lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocessing function for English tweets
def preprocess_english_tweet(tweet):
    # Extract hashtags and mentions
    hashtags = [word.lower() for word in tweet['text'].split() if word.startswith('#')]
    mentions = [word.lower() for word in tweet['text'].split() if word.startswith('@')]

    # Remove mentions and hashtags from the cleaned text
    cleaned_text = tweet['text']
    for element in mentions + hashtags:
        cleaned_text = cleaned_text.replace(element, '')

    # Tokenization with special handling of punctuation-separated words
    tokens = re.findall(r'\w+|\S', cleaned_text)

    # Lemmatization and lowercase conversion
    cleaned_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]

    # Join tokens back into a cleaned text
    cleaned_text = ' '.join(cleaned_tokens)

    # Check if it's a retweet
    is_retweet = tweet['text'].startswith("RT ")

    # Update the tweet dictionary with extracted information
    tweet['cleaned_text'] = cleaned_text
    tweet['hashtags'] = hashtags
    tweet['mentions'] = mentions
    tweet['is_retweet'] = is_retweet




# Define the data directory and the target JSON file
data_directory = "data"
json_filename = "gg2013.json"
json_filepath = os.path.join(data_directory, json_filename)

# Initialize an empty list to store the tweets
tweets = []

# Check if the JSON file exists in the specified directory
if os.path.exists(json_filepath):


    # Open and parse the entire JSON list of tweets
    with open(json_filepath, "r", encoding="utf-8") as json_file:
        try:
            tweets = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")

    # Print the number of tweets loaded
    print(f"Loaded {len(tweets)} tweets from {json_filepath}")

    # Now, 'tweets' contains all the tweets from the JSON file and can be used for preprocessing.
else:
    print(f"The JSON file '{json_filename}' does not exist in the '{data_directory}' directory.")

# Preprocess each tweet in the list
for tweet in tweets:
    preprocess_english_tweet(tweet)

some_tweets = tweets[:20]
for tweet in some_tweets:
  print("")
  print(tweet)
