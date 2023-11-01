import re
from utils.regex import NAME_REGEX, NAME_SLASH_REGEX, NAME_HASHTAG_REGEX, PRESENTERS_REGEX

def extract_presenters(tweets, awards_winners_list):
    """
    Extract presenters associated with specific awards from a list of tweets and organize them by award.

    This function analyzes a list of tweets to identify potential presenters for specific awards. It then organizes the
    presenters by award categories based on the awards provided in the 'awards_winners_list'.

    Parameters:
    - tweets (list of Tweet): A list of Tweet objects containing tweet text.
    - awards_winners_list (dict): A dictionary of award categories as keys and winner names as values.

    Returns:
    - dict: A dictionary where award categories are keys, and the associated presenters are values.
    """

    # A dictionary to store tweets associated with awards
    award_presenter_tweet_dict = {}

    # Generate a list of all the awards names
    existing_awards = []
    for k, v in awards_winners_list.items():
        if v:
            existing_awards.append(k)

    # A list to store presenter-related tweets
    presenter_tweets = []

    # Identify tweets containing presenter mentions, excluding retweets
    for tweet in tweets:
        presenter_tweet = re.search(PRESENTERS_REGEX, tweet.get_original_text())

        if presenter_tweet is None or presenter_tweet.string.startswith("RT"):
            continue
        presenter_tweets.append(presenter_tweet.string)

    # Organize tweets by award categories
    for tweet in presenter_tweets:
        for award in existing_awards:
            if award in tweet:
                if award not in award_presenter_tweet_dict:
                    award_presenter_tweet_dict[award] = []
                award_presenter_tweet_dict[award].append(tweet)

    # A dictionary to store award presenters
    award_presenter = {}

    for award, tweets in award_presenter_tweet_dict.items():
        for tweet in tweets:
            good_matches = []

            # Filter and collect valid presenter mentions
            matches = re.findall(NAME_REGEX, tweet)
            for match in matches:
                if "best" not in match.lower() and "the" not in match.lower():
                    good_matches.append(match)

            # Extract and add additional presenter mentions from slash-separated names
            matches_with_slash = re.findall(NAME_SLASH_REGEX, tweet)
            for match in matches_with_slash:
                if "http" not in match.lower() and "the" not in match.lower():
                    good_matches.extend(match.split("/"))

            # Extract and add presenter mentions from hashtag-annotated names
            matches_with_hashtag = re.findall(NAME_HASHTAG_REGEX, tweet)
            for match in matches_with_hashtag:
                if "golden" not in match.lower() and "globe" not in match.lower() and "the" not in match.lower():
                    good_matches.append(match[1:].strip().strip('.').strip(','))

        award_presenter[award] = good_matches

    return award_presenter
