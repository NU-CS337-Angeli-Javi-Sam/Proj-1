import re
from data_structures.SortedDict import SortedDict
from utils.keywords import PERSON_KEYWORDS
from utils.regex import NOMINEES_REGEX

def extract_nominees(tweets, awards_winners_list):
    """
    Extract nominees associated with specific awards from a list of tweets and organize them by award category.

    This function processes a list of tweets to identify potential nominees for specific awards. It then organizes the
    nominees by award categories, using the provided 'awards_winners_list' to determine the top winners for each award.

    Parameters:
    - tweets (list of Tweet): A list of Tweet objects containing tweet text.
    - awards_winners_list (dict): A dictionary of award categories as keys and winner names as values.

    Returns:
    - dict: A dictionary where award categories are keys, and the associated nominees are organized by their mentions.
    """

    # Filter and keep only existing awards with winners
    existing_awards_winners = {}
    for k, v in awards_winners_list.items():
        if v:
            existing_awards_winners[k] = v

    # A dictionary to store nominees by award category
    awards_nominees = {}

    # Get the list of award categories from the existing winners
    awards = existing_awards_winners.keys()

    for award in awards:
        # Determine the top winner for the current award category
        top_winner = existing_awards_winners[award].getTop(1)[0][0]

        # Initialize a SortedDict to store nominees for the current award category
        awards_nominees[award] = SortedDict()

        for regex in NOMINEES_REGEX:
            # Replace '{Winner}' placeholder in the regex with the top winner's name
            if "{Winner}" in regex:
                regex = regex.replace('{Winner}', top_winner)

            for tweet in tweets:
                # Check if the award name contains any person-related keywords
                if len(list(set(award.split(" ")) & set(PERSON_KEYWORDS))) > 0:
                    # Find all matches in the tweet text using the current regex
                    matches = re.findall(regex, tweet.get_original_text())

                    # Process matches and count mentions
                    for match in matches:
                        if match in awards_nominees[award].getKeys():
                            awards_nominees[award][match] += 1
                        elif "Golden" not in match:
                            awards_nominees[award][match] = 1

    return awards_nominees
