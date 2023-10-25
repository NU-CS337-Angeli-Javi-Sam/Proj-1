from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
import pickle as pkl
import re

# award_references = ["best screenplay - motion picture", "best director - motion picture", "best performance by an actress in a television series - comedy or musical",
#                     "best foreign language film", "best performance by an actor in a supporting role in a motion picture",
#                     "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
#                     "best motion picture - comedy or musical", "best performance by an actress in a motion picture - comedy or musical",
#                     "best mini-series or motion picture made for television", "best original score - motion picture", "best performance by an actress in a television series - drama",
#                     "best performance by an actress in a motion picture - drama", "cecil b. demille award", "best performance by an actor in a motion picture - comedy or musical",
#                     "best motion picture - drama", "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television",
#                     "best performance by an actress in a supporting role in a motion picture", "best television series - drama",
#                     "best performance by an actor in a mini-series or motion picture made for television", "best performance by an actress in a mini-series or motion picture made for television",
#                     "best animated feature film", "best original song - motion picture", "best performance by an actor in a motion picture - drama",
#                     "best television series - comedy or musical", "best performance by an actor in a television series - drama",
#                     "best performance by an actor in a television series - comedy or musical", ]

# Run award regex on tweet text, if match:
# Look through the context to see if any secondary validation regexes pass
# If they pass add the regex to the direction with a vote of 1
# If we find any awards that look similar to our current regex, add vote to that one and dont add new regex
# (Consider those the same award, threshold for similarity is about 70%)

def get_similarity_ratio(text1, text2, words):
    text1 = text1.lower()
    text2 = text2.lower()

    text1 = remove_words(text1, words, ' ')
    text2 = remove_words(text2, words, ' ')

    return SequenceMatcher(None, text1, text2).ratio()
def remove_words(text, words, replacement):
    for word in words:
        if word in text:
            text.replace(word, replacement)
    return text
def remove_endphrase (text, words):
    for word in words:
        if word in text:
            text = text[:text.find(word)]
    return text
def extract_awards(tweets):
    ##[A-za-z]*(award)[A-za-z]*
    # r'#(?i)(?:best)[A-Z][a-zA-Z\s]+' Hashtag regex (?), #...(award) might work for cecil
    # ([A-Z][a-z]* ([aA]ward).*[lL]ifetime)|([lL]ifetime.*([A-Z][a-z]* [aA]ward))
    # (?i) the .* award for lifetime achievement
    unmerged_awards = []
    merged_awards = SortedDict()
    # merged_awards_keywords = {}

    # Didn't get the Best Motion Picture nor Best Performation by Actor/Actress, nor cecil award
    award_regex = r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?'

    validation_regexes = [
        r'(?:won|wins|winning|takes home|takes|gets|got|getting) (?:the\s)?(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?',
        # Wins Regex (Award Object)                             # Win regex, e.g. "X won Y award", "X wins Y award"
        r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)? (?:goes to|is awarded to)']  # Wins Regex (Award Subject)

    # trash_words = ['goes', 'is', 'at', 'for', 'http', 'https', 'on']
    trash_words = [' goes ', ' is ', ' http', ' https', ' for ', ' at ', ' For ', ' At ']
    minor_words = [' in ', ' on ', ' for ', ' a ', ' by ', ' an ', ' or ', ' and ', ' the ', ' nor ', ' yet ', ' but ', ' so ', ' to ', ' from ',
                   ' of ', ' under ', ' over ', ' at ', ' within ', ' between ', ' through ']

    # Remove for only if its an entity as a person or film

    # Regex Validation
    for tweet in tweets:
        # Find instance of potential award mentioning
        regex_matches = re.findall(award_regex, tweet.get_original_text())

        # If there was a mention
        if regex_matches:
            # Do context matching
            for validation_regex in validation_regexes:
                # If context matching succeeds, add to a bucket of each award occurrence
                if re.search(validation_regex, tweet.get_original_text(), re.IGNORECASE):
                    for match in regex_matches:
                        match = remove_endphrase(match, trash_words)

                        temp_match = remove_words(match, minor_words, ' ')

                        if temp_match.istitle():
                            unmerged_awards.insert(0, match)
                        else:
                            unmerged_awards.append(match)

    # print(unmerged_awards)
    for unmerged_award in unmerged_awards:
        merged = False

        for key in merged_awards.getKeys():
            if get_similarity_ratio(unmerged_award, key, minor_words) >= 0.67:
                # merged_awards_keywords[key].add(unmerged_award.strip())
                merged_awards.updateKV_Pair(key, merged_awards.get(key) + 1)
                merged = True
                break
        if not merged:
            merged_awards.add(unmerged_award, 1)
            # merged_awards_keywords[unmerged_award] = set()

    with open('C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\awards.pkl', 'wb') as file:
        pkl.dump(merged_awards, file)

    return merged_awards