import re
import pickle as pkl
from utils.regex import NAME_REGEX, NAME_SLASH_REGEX, NAME_HASHTAG_REGEX

def extract_presenters(tweets, awards_winners_list):
    # with open("C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\award_winners.pkl", "rb") as file:
    #     awards_winners_list = pkl.load(file)

    award_presenter_tweet_dict = {}
    # Remove awards that don't have winners
    existing_awards = []
    for k, v in awards_winners_list.items():
        if v:
            existing_awards.append(k)

    presenters_regex = r'\b[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+\b\s+(presenting|presents|present|announces|announce|introduces|introducing|intros|announcer|announcers)'
    presenter_tweets = []

    for tweet in tweets:
        presenter_tweet = re.search(presenters_regex, tweet.get_original_text())

        if presenter_tweet is None or presenter_tweet.string.startswith("RT"):
            continue
        presenter_tweets.append(presenter_tweet.string)

    for tweet in presenter_tweets:
        for award in existing_awards:
            if award in tweet:
                if award not in award_presenter_tweet_dict:
                    award_presenter_tweet_dict[award] = []
                award_presenter_tweet_dict[award].append(tweet)

    award_presenter = {}
    for award, tweets in award_presenter_tweet_dict.items():
        # print()
        # print(award)
        for tweet in tweets:
            # print(tweet)
            good_matches = []

            matches = re.findall(NAME_REGEX, tweet)
            for match in matches:
                if "best" not in match.lower() and "the" not in match.lower():
                    good_matches.append(match)

            # print("REGULAR", good_matches)

            matches_with_slash = re.findall(NAME_SLASH_REGEX, tweet)
            for match in matches_with_slash:
                if "http" not in match.lower() and "the" not in match.lower():
                    good_matches.extend(match.split("/"))

            # print("SLASH", good_matches)
            # print()

            matches_with_hashtag = re.findall(NAME_HASHTAG_REGEX, tweet)
            for match in matches_with_hashtag:
                if "golden" not in match.lower() and "globe" not in match.lower() and "the" not in match.lower():
                    good_matches.append(match[1:].strip().strip('.').strip(','))

            # print("HASHTAG", good_matches)
        award_presenter[award] = good_matches

    return award_presenter


