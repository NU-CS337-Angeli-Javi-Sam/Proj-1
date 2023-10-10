import os
import json

from helpers.preprocess_tweet import preprocess_tweet

def load_tweets(data_directory, json_filename):

    json_filepath = os.path.join(data_directory, json_filename)

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


    return tweets

def main():
    # Define the data directory and the target JSON file
    data_directory = "data"
    json_filename = "gg2013.json"

    # Initialize an empty list to store the tweets
    tweets = load_tweets(data_directory, json_filename)

    if len(tweets) == 0:
        return
    # Preprocess each tweet in the list
    for tweet in tweets:
        preprocess_tweet(tweet)

    some_tweets = tweets[:20]
    for tweet in some_tweets:
        print("")
        print(tweet)

if __name__ == "__main__":
    main()
