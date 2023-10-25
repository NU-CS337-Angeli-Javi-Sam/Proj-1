import pickle as pkl
import re
from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
def get_similarity_ratio(text1, text2):
    text1 = text1.lower()
    text2 = text2.lower()

    return SequenceMatcher(None, text1, text2).ratio()

def remove_words(text, words, replacement):
    for word in words:
        if word in text:
            text.replace(word, replacement)
    return text

def extract_winners (tweets):
    awards_list = None

    with open("C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\awards.pkl", "rb") as file:
        awards_list = pkl.load(file)

    minor_words = [' in ', ' on ', ' for ', ' a ', ' by ', ' an ', ' or ', ' and ', ' the ', ' nor ', ' yet ', ' but ',
                   ' so ', ' to ', ' from ',
                   ' of ', ' under ', ' over ', ' at ', ' within ', ' between ', ' through ']

    # with open("C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\films_people_2013.pkl", "rb") as file:
    #     films_people_2013 = pkl.load(file)
    #
    # films = films_people_2013['Films']
    # people = films_people_2013['People']


    awards_to_winner = {}

    for key in awards_list.getKeys():
        awards_to_winner[key] = SortedDict()

        winner_regexes = [r'[A-Z][a-zA-Z\s]*[A-Z][a-z]*',
                          r'for ([A-Z][a-z]*\s)+']
        # print(winner_regexes[0])

        for tweet in tweets:
            # award_matches = re.findall(winner_regexes[0], tweet.get_original_text())
            # # print(award_matches)
            #
            # for award_match in award_matches:
            if key in tweet.get_original_text():
                name_matches = []

                for winner_regex in winner_regexes:
                    matches = re.findall(winner_regex, tweet.get_original_text().replace(key, ' '))

                    name_matches.extend(matches)

                for name in name_matches:
                    # official_name = None

                    # if any(['actor', 'actress', 'director']) in key.lower():
                    #     for person in people:
                    #         if get_similarity_ratio(person, name) >= 0.67:
                    #             official_name = person
                    #     break
                    # else:
                    #     for film in films:
                    #         if get_similarity_ratio(film, name) >= 0.8:
                    #             official_name = film
                    # if not official_name:
                    #     continue

                    # print(key, official_name)
                    if name in awards_to_winner[key]:
                       awards_to_winner[key].updateKV_Pair(name, awards_to_winner[key].get(name) + 1)
                    else:
                        if name == 'RT' or name == 'GoldenGlobes':
                            continue
                        # merged = False
                        # for potential_winner in awards_to_winner[key].getKeys():
                        #     if get_similarity_ratio(potential_winner, name) >= 0.67:
                        #         merged = True
                        #         awards_to_winner[key].get(potential_winner).updateKVPair(potential_winner, awards_to_winner[key].get(potential_winner)+1)
                        #

                        awards_to_winner[key].add(name, 1)


    # Note to Sam: Change this loop to remove all the keys that satisfy if statement
    for k, v in awards_to_winner.items():
        if len(v.getKeys()) <= 0:
            continue
        print(k, v)

    # print(awards_to_winner.keys())
    # print(awards_to_winner['Best Original Song'])


