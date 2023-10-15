import os
import json
import re
import sys

from data_structures.Award import Award
from data_structures.AwardsCeremony import AwardsCeremony
from data_structures.Entity import Entity
from data_structures.Tweet import Tweet
from data_structures.TweetStats import TweetStats

from helpers.awards import get_awards_list
from helpers.hosts import find_hosts_in_tweets, get_hosts_list
from helpers.nominees import get_nominees_dict
from helpers.presenters import get_presenters_dict
from helpers.winner import get_winners_dict


def initialization_script():
    filename = sys.argv[1] if len(sys.argv) > 1 else "gg2013.json"  # First argument
    year = sys.argv[2] if len(sys.argv) > 2 else "2013"  # Second argument

    return filename, year


def load_tweet_data(data_directory, filename):
    filepath = os.path.join(data_directory, filename)

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


def print_test_info(tweets):
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

    sample_award = Award(
        "best screenplay - motion picture",
        ["robert pattinson", "amanda seyfried"],
        ["zero dark thirty", "lincoln", "silver linings playbook", "argo"],
        "argo",
    )

    print(sample_award)

    print("")
    print("Sample Awards Ceremony:")

    sample_awards_ceremony = AwardsCeremony(
        "Golden Globes",
        "Madison Square Garden",
        "9:00pm",
        "11:00pm",
        ["amy poehler", "tina fey"],
        [sample_award],
    )

    print(sample_awards_ceremony)
    print(sample_awards_ceremony.to_json())

    # print("")
    # print("")
    # print("")
    # print("Testing API")
    # print("These are the awards: ", get_awards("2020", sample_awards_ceremony))
    # print("These are the hosts: ", get_hosts("2020", sample_awards_ceremony))
    # print("These are the presenters: ", get_presenters("2020", sample_awards_ceremony))
    # print("These are the nominees: ", get_nominees("2020", sample_awards_ceremony))
    # print("These are the winners: ", get_winner("2020", sample_awards_ceremony))


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

    hosts = find_hosts_in_tweets(tweets)

    test_stats = TweetStats()

    # for tweet in tweets[10000:10040]:
    #     print("")
    #     print("original tweet:", tweet.get_original_text())
    #     print(tweet.get_tokens())

    for tweet in tweets:
        test_stats.analyzeTweet(tweet)

    print('\n' + str(test_stats))

    # tweets = [tweet for tweet in tweets if not tweet.is_retweet() and not tweet.has_emojis()]

    # tweets = [tweet for tweet in tweets if tweet.get_language() == 'en']

    # print(f"Number of English non retweets without emojis: {len(tweets)}")

    sample_award = Award("best screenplay - motion picture", [
        "robert pattinson",
        "amanda seyfried"
      ], [
        "zero dark thirty",
        "lincoln",
        "silver linings playbook",
        "argo"
      ], "argo" )

    sample_award_2 = Award("best performance by an actor in a supporting role in a series, mini-series or motion picture made for television",[
        "kristen bell",
        "john krasinski"
      ], [
        "max greenfield",
        "danny huston",
        "mandy patinkin",
        "eric stonestreet"
      ], "ed harris")

    sample_awards_ceremony = AwardsCeremony(hosts, [sample_award, sample_award_2])

    with open(text_output_filepath, "w") as file:
        file.write(str(sample_awards_ceremony))

    with open(json_output_filepath, "w") as file:
        json.dump(sample_awards_ceremony.to_json(), file)


if __name__ == "__main__":
    main()
