import pickle as pkl
import re
from data_structures.SortedDict import SortedDict


def extract_winners (tweets):
    awards_list = None

    with open("C:/Users/samj9/Desktop/awards.pkl", "rb") as file:
        awards_list = pkl.load(file)

    awards_to_winner = {}

    for key in awards_list.getKeys():
        awards_to_winner[key] = SortedDict()

        winner_regexes = [r"[A-Z][a-zA-Z\s]+"]
        # print(winner_regexes[0])

        for tweet in tweets:
            # award_matches = re.findall(winner_regexes[0], tweet.get_original_text())
            # # print(award_matches)
            #
            # for award_match in award_matches:
            if key in tweet.get_original_text():
                name_matches = re.findall(r"[A-Z][a-zA-Z\s]*[A-Z][a-z]*",tweet.get_original_text().replace(key, ' '))

                for name in name_matches:
                    if name in awards_to_winner[key]:
                       awards_to_winner[key].updateKV_Pair(name, awards_to_winner[key].get(name) + 1)
                    else:
                        if name == 'RT' or name == 'GoldenGlobes':
                            continue
                        awards_to_winner[key].add(name, 1)

    for k, v in awards_to_winner.items():
        print(k, v.getTop(5))

    # print(awards_to_winner)



