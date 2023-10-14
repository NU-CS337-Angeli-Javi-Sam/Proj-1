import re
from .import_awards_ceremony import import_awards_ceremony


def find_opening_monologue(tweet):
    tweet_text = tweet.get_original_text()

    opening_monologue_regex = re.compile("[A-Z][a-z]* [A-Z][a-z]*.*(?i:opening monologue)")
    opening_monologue_match = opening_monologue_regex.search(tweet_text)
    if opening_monologue_match != None:
        opening_monologue_match = opening_monologue_match.string

    return tweet_text


def find_host(tweet):
    tweet_text = tweet.get_original_text()

    host_regex = re.compile("host [A-Z][a-z]* [A-Z][a-z]*")
    host_name_regex = re.compile("[A-Z][a-z]* [A-Z][a-z]*")

    possible_host_match = host_regex.search(tweet_text)


    possible_host_name = None
    if possible_host_match != None:
        match_start = possible_host_match.start()
        match_end = possible_host_match.end()
        possible_host_name = host_name_regex.search(tweet_text[match_start + 5: match_end]).string
        if "Golden" in possible_host_name or "Globes" in possible_host_name:
            return None

    return possible_host_name



def find_hosts_in_tweets(tweets):

    possible_hosts = {}

    for tweet in tweets:
        possible_host_name = find_host(tweet)
        if possible_host_name != None:
            if possible_host_name not in possible_hosts:
                possible_hosts[possible_host_name] = 0
            possible_hosts[possible_host_name] += 1

            for host_name in possible_hosts:
                if host_name != possible_host_name and host_name in tweet.get_original_text():
                    if possible_host_name not in possible_hosts:
                        possible_hosts[possible_host_name] = 0
                    possible_hosts[possible_host_name] += 1

    for tweet in tweets:
        opening_monologue_mention = find_opening_monologue(tweet)
        if opening_monologue_mention != None:
            for host in possible_hosts:
                if host in opening_monologue_mention:
                    possible_hosts[host] += 1


    sorted_possible_hosts = sorted(possible_hosts.items(), key=lambda item: item[1], reverse=True)
    return [sorted_possible_hosts[0][0], sorted_possible_hosts[1][0]]


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
