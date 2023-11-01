from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
import re
from utils.regex import WINNERS_REGEX

def get_similarity_ratio(text1, text2):
    """
    Compute the similarity ratio between two text strings after converting them to lowercase.

    Parameters:
    - text1 (str): The first text string.
    - text2 (str): The second text string.

    Returns:
    - float: The similarity ratio between the two text strings, ranging from 0 to 1.
    """
    text1 = text1.lower()
    text2 = text2.lower()
    return SequenceMatcher(None, text1, text2).ratio()

def merge(lst):
    """
    Merge similar keys in a sorted dictionary.

    This function iterates through the keys in a sorted dictionary and merges keys that have a similarity ratio
    greater than or equal to 0.67. Merging is done by combining the values of similar keys and setting one of
    the keys' value to 0.

    Parameters:
    - list (SortedDict): A SortedDict containing keys to be merged.

    Returns:
    - SortedDict: A SortedDict with merged keys.
    """

    # Get the sorted keys from the input SortedDict.
    keys = lst.getSortedKeys()

    # Initialize a list to keep track of merged keys.
    merged = []

    # Iterate through each key in the sorted dictionary.
    for key in keys:
        # Iterate through subsequent keys for comparison.
        for other_key in keys[keys.index(key) + 1:]:
            # Skip already merged keys.
            if other_key in merged:
                continue

            # Check the similarity between the current key and other_key.
            if get_similarity_ratio(key, other_key) >= 0.67:
                # Combine the values of similar keys.
                lst[key] += lst[other_key]

                # Set the value of other_key to 0 to indicate merging.
                lst[other_key] = 0

                # Record the merged key to avoid redundant merging.
                merged.append(other_key)

    # Return the SortedDict with merged keys.
    return lst

def extract_winners (tweets, awards_list):
    """
    Extract award winners from a list of tweets and compile them into a dictionary.

    This function processes a list of tweets to identify mentions of award winners based on predefined regular expressions.
    The identified winners are organized into a dictionary where keys are award names, and values are SortedDicts
    containing winners and their respective frequencies.

    Parameters:
    - tweets (list of Tweet): A list of Tweet objects containing tweet data.
    - awards_list (SortedDict): A SortedDict of award names.

    Returns:
    - dict: A dictionary mapping award names to SortedDicts of award winners and their frequencies.
    """

    awards_to_winner = {}  # Create an empty dictionary to store award winners.

    # Iterate through each award in the provided awards list.
    for key in awards_list.getKeys():
        awards_to_winner[key] = SortedDict()  # Initialize a SortedDict for each award.

        # Iterate through each tweet to search for mentions of the current award.
        for tweet in tweets:
            if key in tweet.get_original_text():
                regex_matches = []  # Create a list to store regex matches.

                # Iterate through regular expressions designed to capture award winners.
                for winner_regex in WINNERS_REGEX:
                    matches = re.findall(winner_regex, tweet.get_original_text().replace(key, ' '))

                    regex_matches.extend(matches)  # Add matches to the list.

                # Iterate through each match and update the winner dictionary.
                for match in regex_matches:
                    if match in awards_to_winner[key]:
                        awards_to_winner[key].updateKV_Pair(match, awards_to_winner[key].get(match) + 1)
                    else:
                        # Exclude unwanted matches.
                        if match == 'RT' or match == 'GoldenGlobes' or match == 'Golden Globes':
                            continue
                        awards_to_winner[key].add(match, 1)

    keys = list(awards_to_winner.keys())  # Get a list of award names from the dictionary.
    relevant_awards = []  # Create a list to store relevant awards.

    # Filter awards with at least 3 winners and a name length greater than 5.
    for key in keys:
        if len(awards_to_winner[key].getKeys()) >= 3 and len(key) > 5:
            relevant_awards.append(key)

    # Merge similar winners for each relevant award.
    for award in relevant_awards:
        awards_to_winner[award] = merge(awards_to_winner[award])

    return awards_to_winner  # Return the dictionary of award winners.
