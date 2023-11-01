from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
import re
from utils.regex import WINNERS_REGEX

# Finding out if winner is supposed to be a person:
# Congrats person for thing: if person look for before the for and
# if not look what's after the for
# Give priority for unigrams for movies and give bigrams for people
# Give priority for unigram hashtags for movies perhaps
# Give priority for regexes that read Blank wins

#Gets the similarity ratio between two pieces of text
def get_similarity_ratio(text1, text2):
    text1 = text1.lower()
    text2 = text2.lower()

    return SequenceMatcher(None, text1, text2).ratio()

# Removes
def remove_words(text, words, replacement):
    for word in words:
        if word in text:
            text.replace(word, replacement)
    return text

#Removes
def remove_endphrase (text, words):
    for word in words:
        if word in text:
            text = text[:text.find(word)]
    return text

#Removes
def remove_frontphrase (text, words):
    for word in words:
        if word in text:
            text = text[text.find(word):]
    return text

def merge (list):
    keys = list.getSortedKeys()
    merged = []

    for key in keys:
        for other_key in keys[keys.index(key)+1:]:
            if other_key in merged:
                continue
            if get_similarity_ratio(key, other_key) >= 0.67:
                list[key] += list[other_key]
                list[other_key] = 0
                merged.append(other_key)
    return list


def extract_winners (tweets, awards_list):

    #Extract awards from the output of the extract_awards method

    #Dict mapping awards to potential winners, keys are winners, values are sort dictionaries of winner candidates
    awards_to_winner = {}

    for key in awards_list.getKeys():
        awards_to_winner[key] = SortedDict()


        for tweet in tweets:
            #If tweet is relevant to our current award (the current key)
            if key in tweet.get_original_text():
                regex_matches = []

                #Find all the matches to our regexes for this particular tweet
                for winner_regex in WINNERS_REGEX:
                    matches = re.findall(winner_regex, tweet.get_original_text().replace(key, ' '))

                    regex_matches.extend(matches)

                #Check if any of the matches are already mapped to an award key in awards_to_winner
                #If so, increment the preexisting match, if not add it
                for match in regex_matches:

                    if match in awards_to_winner[key]:
                       awards_to_winner[key].updateKV_Pair(match, awards_to_winner[key].get(match) + 1)
                    else:
                        #Adds match, removes RT or GoldenGlobes trash entries
                        if match == 'RT' or match == 'GoldenGlobes' or match == 'Golden Globes':
                            continue
                        awards_to_winner[key].add(match, 1)


    #Removes all awards that don't have winners or only have a few "winner" mentions
    #Merges alike winners for
    keys = list(awards_to_winner.keys())
    relevant_awards = []

    #Attempt to remove irrelevant awards
    for key in keys:
        if len(awards_to_winner[key].getKeys()) >= 3:
            if len(key) > 5:
                relevant_awards.append(key)

    for award in relevant_awards:
        awards_to_winner[award] = merge(awards_to_winner[award])



    return awards_to_winner
