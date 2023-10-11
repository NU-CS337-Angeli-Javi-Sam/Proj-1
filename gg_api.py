import os
import json

from data_structures.Award import Award
from data_structures.AwardsCeremony import AwardsCeremony
from data_structures.Entity import Entity
from data_structures.Tweet import Tweet

from helpers.awards import get_awards_list
from helpers.hosts import get_hosts_list
from helpers.nominees import get_nominees_dict
from helpers.presenters import get_presenters_dict
from helpers.winner import get_winners_dict

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

    print("")
    print("Sample Awards Ceremony:")

    sample_awards_ceremony = AwardsCeremony("Golden Globes", "Madison Square Garden", "9:00pm", "11:00pm", ["amy poehler", "tina fey"], [sample_award])

    print(sample_awards_ceremony)
    print(sample_awards_ceremony.to_json())

    print("")
    print("")
    print("")
    print("Testing API")
    print("These are the awards: ", get_awards("2020", sample_awards_ceremony))
    print("These are the hosts: ", get_hosts("2020", sample_awards_ceremony))
    print("These are the presenters: ", get_presenters("2020", sample_awards_ceremony))
    print("These are the nominees: ", get_nominees("2020", sample_awards_ceremony))
    print("These are the winners: ", get_winner("2020", sample_awards_ceremony))

def get_hosts(year, awards_ceremony):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    return get_hosts_list(awards_ceremony)

def get_awards(year, awards_ceremony):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    return get_awards_list(awards_ceremony)

def get_nominees(year, awards_ceremony):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    return get_nominees_dict(awards_ceremony)

def get_winner(year, awards_ceremony):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    return get_winners_dict(awards_ceremony)

def get_presenters(year, awards_ceremony):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    return get_presenters_dict(awards_ceremony)

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    pass

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Define the data directory and the target JSON file
    data_directory = "data"
    json_filename = "gg2013.json"

    # Initialize an empty list to store the tweets
    tweet_data = load_tweet_data(data_directory, json_filename)

    if len(tweet_data) == 0:
        return

    tweets = create_tweet_objects(tweet_data)

    print(f"Number of tweets: {len(tweets)}")

    tweets = [tweet for tweet in tweets if not tweet.is_retweet() and not tweet.has_emojis()]

    # tweets = [tweet for tweet in tweets if tweet.get_language() == 'en']

    print(f"Number of English non retweets without emojis: {len(tweets)}")


if __name__ == "__main__":
    main()
