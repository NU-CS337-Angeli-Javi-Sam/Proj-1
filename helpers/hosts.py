import re
from utils.import_awards_ceremony import import_awards_ceremony
from utils.regex import HOST_REGEX, NAME_REGEX, OPENING_MONOLOGUE_REGEX

def find_opening_monologue_mention(tweet):
    """
    Find a mention of the opening monologue in a tweet's text.

    This function searches for a mention of an opening monologue in the text of a tweet using the provided regular expression.

    Parameters:
    - tweet: A Tweet object containing text to search.

    Returns:
    - opening_monologue_match_mention: The text of the tweet that mentions the opening monologue if found, or None if not found.
    """
    tweet_text = tweet.get_original_text()

    # Define a regular expression pattern for matching opening monologue mentions
    opening_monologue_regex = re.compile(OPENING_MONOLOGUE_REGEX)

    # Search for the opening monologue mention in the tweet's text
    opening_monologue_match = opening_monologue_regex.search(tweet_text)

    # If a match is found, extract the matched text, else return None
    opening_monologue_match_mention = opening_monologue_match.group() if opening_monologue_match is not None else None

    return opening_monologue_match_mention


def find_host_names(tweet):
    """
    Find the names of hosts mentioned in a tweet.

    This function searches for mentions of hosts in the text of a tweet using the provided regular expressions.

    Parameters:
    - tweet: A Tweet object containing text to search.

    Returns:
    - possible_host_name: The name of the host mentioned in the tweet if found, or None if not found.
    """
    tweet_text = tweet.get_original_text()

    # Define regular expression patterns for matching host mentions and host names
    host_regex = re.compile(HOST_REGEX)
    host_name_regex = re.compile(NAME_REGEX)

    # Search for a possible host mention in the tweet's text
    possible_host_match = host_regex.search(tweet_text)

    possible_host_name = None

    # If a possible host mention is found, extract the host name
    if possible_host_match is not None:
        match_start = possible_host_match.start()
        match_end = possible_host_match.end()

        # Extract and process the possible host name
        possible_host_name = host_name_regex.search(tweet_text[match_start + 5: match_end]).group()

        # Check if the possible host name contains unwanted terms (e.g., "Golden" or "Globes")
        if "Golden" in possible_host_name or "Globes" in possible_host_name:
            return None

    return possible_host_name


def find_hosts_in_tweets(tweets):
    """
    Find possible hosts mentioned in a list of tweets and identify the top two likely hosts.

    Parameters:
    - tweets: A list of Tweet objects containing text to search for host mentions.

    Returns:
    - hosts: A list of the top two likely hosts mentioned in the tweets.

    This function iterates through a list of tweets and identifies possible hosts by searching for
    their names. It counts the number of times each possible host is mentioned and identifies
    the top two hosts with the highest mention counts. It also considers tweets mentioning
    the opening monologue.

    Example usage:
    >>> tweets = [tweet1, tweet2, tweet3]
    >>> likely_hosts = find_hosts_in_tweets(tweets)
    >>> print(likely_hosts)

    Output:
    ['John Smith', 'Jane Doe']
    """

    possible_hosts = {} # Dictionary to store possible hosts and their mention counts.

    # Iterate through the list of tweets to find possible hosts.
    for tweet in tweets:
        possible_host_name = find_host_names(tweet)
        if possible_host_name != None:
            if possible_host_name not in possible_hosts:
                possible_hosts[possible_host_name] = 0
            possible_hosts[possible_host_name] += 1

            for host_name in possible_hosts:
                if host_name != possible_host_name and host_name in tweet.get_original_text():
                    if possible_host_name not in possible_hosts:
                        possible_hosts[possible_host_name] = 0
                    possible_hosts[possible_host_name] += 1

    # Iterate through the tweets again to consider opening monologue mentions.
    for tweet in tweets:
        opening_monologue_mention = find_opening_monologue_mention(tweet)
        if opening_monologue_mention != None:
            for host in possible_hosts:
                if host in opening_monologue_mention:
                    possible_hosts[host] += 1

    # Sort the possible hosts by mention count in descending order.
    sorted_possible_hosts = sorted(possible_hosts.items(), key=lambda item: item[1], reverse=True)

    # Identify the top two likely hosts.
    likely_hosts = [sorted_possible_hosts[0][0], sorted_possible_hosts[1][0]]
    return likely_hosts


def get_hosts_list(year):
    """
    Get the list of hosts for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the hosts.

    Returns:
    - hosts (list): A list of hosts for the specified awards ceremony year.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Retrieve the list of hosts from the awards ceremony data.
    hosts = awards_ceremony.get("Host", [])

    return hosts
