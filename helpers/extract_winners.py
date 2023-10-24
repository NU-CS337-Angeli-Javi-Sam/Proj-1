import pickle as pkl
import re
from data_structures.SortedDict import SortedDict


def extract_winners (tweets):
    awards_list = None

    with open("C:/Users/samj9/Desktop/awards.pkl", "rb") as file:
        awards_list = pkl.load(file)

    awards_to_winner = {}

    for key in awards_list.getKeys():
        awards_to_winner[key] = {}

        winner_regexes = [r"[A-Z][a-zA-Z\s]+ (i?)(Best Director)"]
        # print(winner_regexes[0])

        for tweet in tweets:
            award_matches = re.findall(winner_regexes[0], tweet.get_original_text())
            print(award_matches)

            for award_match in award_matches:
                print('hello', award_match)
                name_matches = re.findall(r'[A-Z][a-zA-Z\\s]+',award_match.replace(key, ' '))

                print(str(award_match),name_matches)

    # print(awards_to_winner)



