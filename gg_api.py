import os
import json
from data_structures.Award import Award
from data_structures.Entity import Entity
from data_structures.Tweet import Tweet

def load_tweet_data(data_directory, json_filename):

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

def get_hosts(year):
    pass

def get_awards(year):
    pass

def get_nominees(year):
    pass

def get_winner(year):
    pass

def get_presenters(year):
    pass

def pre_ceremony():
    pass

def main():
    # Define the data directory and the target JSON file
    data_directory = "data"
    json_filename = "gg2013.json"

    # Initialize an empty list to store the tweets
    tweet_data = load_tweet_data(data_directory, json_filename)

    if len(tweet_data) == 0:
        return

    tweets = []
    # Preprocess each tweet in the list
    for tweet in tweet_data:
      new_tweet = Tweet(tweet)
      tweets.append(new_tweet)

    some_tweets = tweets[:20]
    for tweet in some_tweets:
        print("")
        print(tweet)
        # print(tweet.get_tokens())


    print("")
    print("Sample Entity:")

    sample_entity = Entity("My name")
    sample_entity.set_name("Javi")

    print(sample_entity)

    print("")
    print("Sample Award:")

    sample_award = Award("best screenplay - motion picture", [
        "robert pattinson",
        "amanda seyfried"
      ], [
        "zero dark thirty",
        "lincoln",
        "silver linings playbook",
        "argo"
      ], "argo" )

    print(sample_award)


if __name__ == "__main__":
    main()