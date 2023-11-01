import os
import json
import sys

from data_structures.Award import Award
from data_structures.AwardsCeremony import AwardsCeremony
from data_structures.Tweet import Tweet
from data_structures.TweetStats import TweetStats

from helpers.awards import get_awards_list
from helpers.hosts import get_hosts_list
from helpers.nominees import get_nominees_dict
from helpers.presenters import get_presenters_dict
from helpers.winner import get_winners_dict

from extractors.extract_winners import extract_winners
from extractors.extract_awards import extract_awards
from extractors.extract_nominees import extract_nominees
from extractors.extract_presenters import extract_presenters
from extractors.extract_hosts import extract_hosts
from extractors.extract_more import extract_more_info

def initialization_script():
    """
    Initialize script parameters based on command line arguments or default values.

    This function is used to set the `filename` and `year` based on command line arguments.
    If the script is executed with command line arguments, it uses the provided values.
    If no command line arguments are given, default values are used.

    Returns:
    - str: The filename for the data file to be processed.
    - str: The year associated with the data file.
    """

    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]  # The first argument is the filename
    else:
        # If no argument is provided, use a default filename
        filename = "gg2013.json"

    # Check if the second command line argument is provided (year)
    if len(sys.argv) > 2:
        year = sys.argv[2]  # The second argument is the year
    else:
        # If no argument is provided, use a default year
        year = "2013"

    return filename, year

def load_tweets_from_json(data_directory, filename):
    """
    Load tweets from a JSON file located in the specified directory.

    This function constructs the file path by joining the data directory and the given filename.
    It attempts to open and parse the JSON file, extracting a list of tweets from it.
    If the file exists and can be successfully loaded, it returns the list of tweets.
    Otherwise, it prints error messages and returns an empty list.

    Parameters:
    - data_directory (str): The directory where the JSON file is located.
    - filename (str): The name of the JSON file to be loaded.

    Returns:
    - list: A list of tweets loaded from the JSON file or an empty list if there was an error.
    """
    filepath = os.path.join(data_directory, filename)
    print(f"Loading tweets from {filepath}")

    tweets = []

    # Check if the JSON file exists in the specified directory
    if os.path.exists(filepath):
        # Open and parse the entire JSON list of tweets
        with open(filepath, "r", encoding="utf-8") as json_file:
            try:
                tweets = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")

        print(f"Loaded {len(tweets)} tweets from {filepath}")
    else:
        print(
            f"The JSON file '{filename}' does not exist in the '{data_directory}' directory."
        )

    return tweets

def create_tweet_objects(tweet_data):
    """
    Create a list of Tweet objects from raw tweet data.

    This function takes a list of raw tweet data and creates Tweet objects for each tweet in the list.
    It iterates through the tweet data and creates a new Tweet object for each tweet, storing them in a list.

    Parameters:
    - tweet_data (list): A list of raw tweet data.

    Returns:
    - list of Tweet: A list of Tweet objects representing the tweets in the input data.
    """
    tweets = []

    # Preprocess each tweet in the list
    for tweet in tweet_data:
        new_tweet = Tweet(tweet)
        tweets.append(new_tweet)

    return tweets

def analyze_tweets(tweets):
    """
    Analyze a list of tweets and return tweet statistics.

    This function takes a list of tweet objects, logs each tweet's information into a TweetStats object,
    analyzes the tweet data, and sets a parameter 'K' for the number of top items to retrieve. Finally, it returns
    the TweetStats object containing tweet statistics.

    Parameters:
    - tweets (list of Tweet): A list of Tweet objects to be analyzed.

    Returns:
    - TweetStats: An object containing tweet statistics.
    """

    tweet_stats = TweetStats()

    for tweet in tweets:
        tweet_stats.logTweet(tweet)

    tweet_stats.analyzeTweets()
    tweet_stats.setK(10)
    return tweet_stats

def compile_data(hosts, awards_winners, awards_presenters, awards_nominees, tweet_stats):
    good_awards = []
    for award_name in awards_winners.keys():

        try:
            presenters = awards_presenters[award_name]
        except:
            presenters = []

        try:
            nominees = [a[0] for a in awards_nominees[award_name].getTop(5)]
        except:
            nominees = []

        try:
            winner = awards_winners[award_name].getTop(1)[0][0]
        except:
            winner = ""

        award_item = Award(award_name, presenters, nominees, winner)
        good_awards.append(award_item)

    return AwardsCeremony(hosts, good_awards, tweet_stats)

def print_files(text_output_filepath, json_output_filepath, good_awards_ceremony):
    with open(text_output_filepath, "w") as file:
        file.write(str(good_awards_ceremony))

    with open(json_output_filepath, "w") as file:
        json.dump(good_awards_ceremony.to_json(), file)

def get_hosts(year):
    """Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns."""
    return get_hosts_list(year)

def get_awards(year):
    """Awards is a list of strings. Do NOT change the name
    of this function or what it returns."""
    return get_awards_list(year)

def get_nominees(year):
    """Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns."""
    return get_nominees_dict(year)

def get_winner(year):
    """Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns."""
    return get_winners_dict(year)

def get_presenters(year):
    """Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns."""
    return get_presenters_dict(year)

def pre_ceremony():
    """This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns."""
    pass

def main():
    """This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns."""

    input_directory = "data"
    output_directory = "output"

    filename, year = initialization_script()

    text_output_filepath = f"{output_directory}/output{year}.txt"
    json_output_filepath = f"{output_directory}/output{year}.json"

    print()
    tweet_data = load_tweets_from_json(input_directory, filename)
    if len(tweet_data) == 0:
        return
    print()

    print("Creating Tweet Objects")
    tweets = create_tweet_objects(tweet_data)
    print("Tweet Objects Created")
    print()

    print("Analyzing Tweets")
    tweet_stats = analyze_tweets(tweets)
    print("Tweets Analyzed")
    print()

    print("Identifying Hosts")
    hosts = extract_hosts(tweets)
    print("Hosts Identified")
    print()

    print("Extracting Awards")
    awards = extract_awards(tweets)
    print("Awards Extracted")
    print()

    print("Extracting Winners")
    awards_winners = extract_winners(tweets, awards)
    print("Winners Extracted")
    print()

    print("Extracting Nominees")
    awards_nominees = extract_nominees(tweets, awards_winners)
    print("Nominees Extracted")
    print()

    print("Extracting Presenters")
    awards_presenters = extract_presenters(tweets, awards_winners)
    print("Presenters Extracted")
    print()

    print("Compiling Data")

    good_awards_ceremony = compile_data(hosts, awards_winners, awards_presenters, awards_nominees, tweet_stats)

    # good_awards = []
    # for award_name in awards_winners.keys():

    #     try:
    #         presenters = awards_presenters[award_name]
    #     except:
    #         presenters = []

    #     try:
    #         nominees = [a[0] for a in awards_nominees[award_name].getTop(5)]
    #     except:
    #         nominees = []

    #     try:
    #         winner = awards_winners[award_name].getTop(1)[0][0]
    #     except:
    #         winner = ""

    #     award_item = Award(award_name, presenters, nominees, winner)
    #     good_awards.append(award_item)

    # good_awards_ceremony = AwardsCeremony(hosts, good_awards, tweet_stats)

    # with open("PICKLED_STUFF.pkl", 'wb') as file:
    #     pkl.dump(good_awards_ceremony, file)
    #     pkl.dump(tweets, file)

    # exit(0)

    # extract_more_info(tweets, good_awards_ceremony.get_awards())

    print("Data Compiled")
    print()

    print("Writing Data")
    print_files(text_output_filepath, json_output_filepath, good_awards_ceremony)
    print("Data Written")

if __name__ == "__main__":
    main()
