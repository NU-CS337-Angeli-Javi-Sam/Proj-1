import os
import json
import sys

from data_structures.Award import Award
from data_structures.AwardsCeremony import AwardsCeremony
from data_structures.Tweet import Tweet
from data_structures.TweetStats import TweetStats

from helpers.awards import get_awards_list
from helpers.hosts import find_hosts_in_tweets, get_hosts_list
from helpers.nominees import get_nominees_dict
from helpers.presenters import get_presenters_dict
from helpers.winner import get_winners_dict

from extractors.extract_winners import extract_winners
from extractors.extract_awards import extract_awards
from extractors.extract_nominees import extract_nominees
from extractors.extract_presenters import extract_presenters

import pickle as pkl

def initialization_script():
    filename = sys.argv[1] if len(sys.argv) > 1 else "gg2013.json"  # First argument
    year = sys.argv[2] if len(sys.argv) > 2 else "2013"  # Second argument

    return filename, year

def load_tweet_data(data_directory, filename):
    filepath = os.path.join(data_directory, filename)
    print(filepath)

    tweets = []

    # Check if the JSON file exists in the specified directory
    if os.path.exists(filepath):
        # Open and parse the entire JSON list of tweets
        with open(filepath, "r", encoding="utf-8") as json_file:
            try:
                tweets = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")

        # Print the number of tweets loaded
        print(f"Loaded {len(tweets)} tweets from {filepath}")
        # Now, 'tweets' contains all the tweets from the JSON file and can be used for preprocessing.
    else:
        print(
            f"The JSON file '{filename}' does not exist in the '{data_directory}' directory."
        )

    return tweets

def create_tweet_objects(tweet_data):
    tweets = []

    # Preprocess each tweet in the list
    for tweet in tweet_data:
        new_tweet = Tweet(tweet)
        tweets.append(new_tweet)

    return tweets

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

    tweet_data = load_tweet_data(input_directory, filename)

    if len(tweet_data) == 0:
        return

    tweets = create_tweet_objects(tweet_data)

    print("Creating Tweet Objects")

    tweet_stats = TweetStats()

    print("Tweet Objects Created")
    print()

    for tweet in tweets:
        tweet_stats.logTweet(tweet)

    print("Analyzing Tweets")

    tweet_stats.analyzeTweets()

    print("Tweets Analyzed")
    print()

    tweet_stats.setK(10)

    print("Identifying Hosts")

    hosts = find_hosts_in_tweets(tweets)

    print("Hosts Identified")
    print()

    #Extraction:
    print("Extracting Awards")
    awards = extract_awards(tweets) # SortedDict("award", count)
    print("Awards Extracted")
    print()

    print("Extracting Winners")
    awards_winners = extract_winners(tweets, awards) # {"award": SortedDict("potential winners", count)}
    print("Winners Extracted")
    print()

    print("Extracting Nominees")
    awards_nominees = extract_nominees(tweets, awards_winners) # {"award": SortedDict("potential nominees", count)}
    print("Nominees Extracted")
    print()
    print("Extracting Presenters")
    awards_presenters = extract_presenters(tweets, awards_winners) # {"award": ["presenters"]}
    print("Presenters Extracted")

    print("Compiling Data")
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

    good_awards_ceremony = AwardsCeremony(hosts, good_awards, tweet_stats)

    print("Data Compiled")

    print("Writing Data")

    with open(text_output_filepath, "w") as file:
        file.write(str(good_awards_ceremony))

    with open(json_output_filepath, "w") as file:
        json.dump(good_awards_ceremony.to_json(), file)

    print("Data Written")
if __name__ == "__main__":
    main()
