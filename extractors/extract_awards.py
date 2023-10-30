from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
import pickle as pkl
import re
from utils.keywords import award_keywords

"""
Extract awards method
    Given: Tweet Objects
    Returns: SortDict of Award_names to Confidence Vote
"""

# Potential ideas for cecildemille
# ([A-Z][a-z]* ([aA]ward).*[lL]ifetime)|([lL]ifetime.*([A-Z][a-z]* [aA]ward))
# (?i) the .* award for lifetime achievement


#Gets the similarity ratio between 2 strings
def get_similarity_ratio(text1, text2, words):
    text1 = text1.lower()
    text2 = text2.lower()

    text1 = remove_words(text1, words, ' ')
    text2 = remove_words(text2, words, ' ')

    return SequenceMatcher(None, text1, text2).ratio()

#
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
        unmerged_awards = []
        merged_awards = SortedDict()

        award_regexes = [
            r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?',
            r'[lL]ifetime [aA]chievement [aA]ward'
        ]

        validation_regexes = [
            r'(?:won|wins|winning|takes home|takes|gets|got|getting) (?:the\s)?(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?',# Wins Regex (Award Object)
            r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)? (?:goes to|is awarded to)',  # Wins Regex (Award Subject)
            r'[lL]ifetime [aA]chievement [aA]ward'] #Accepts regex for Cecil B. Award

        # trash_words = ['goes', 'is', 'at', 'for', 'http', 'https', 'on']
        trash_words = [' goes ', ' is ', ' http', ' https', ' for ', ' at ', ' For ', ' At ']
        minor_words = [' in ', ' on ', ' for ', ' a ', ' by ', ' an ', ' or ', ' and ', ' the ', ' nor ', ' yet ', ' but ', ' so ', ' to ', ' from ',
                       ' of ', ' under ', ' over ', ' at ', ' within ', ' between ', ' through ']
        # Regex Validation
        for tweet in tweets:
            # Find instance of potential award mentioning
            regex_matches = []
            for award_regex in award_regexes:

                matches = re.findall(award_regex, tweet.get_original_text())

                # if award_regex == r'[lL]ifetime [aA]chievement [aA]ward' and matches:
                #     print(matches)

                regex_matches.extend(matches)

            # if  'Lifetime Achievement Award' in regex_matches:
            #     print('here')
            # If there was a mention
            if regex_matches:
                # Do context matching
                for validation_regex in validation_regexes:
                    # If context matching succeeds, add to a bucket of each award occurrence
                    if re.search(validation_regex, tweet.get_original_text(), re.IGNORECASE):
                        for match in regex_matches:
                            # if 'lifetime' in match.lower():
                            #     print(match)

                            match = remove_endphrase(match, trash_words)

                            temp_match = remove_words(match, minor_words, ' ')

                            if temp_match.istitle():
                                unmerged_awards.insert(0, match)
                            else:
                                unmerged_awards.append(match)

        for unmerged_award in unmerged_awards:
            # print(unmerged_award)

            valid = False

            for keyword in award_keywords:
                if keyword in unmerged_award.lower():
                    valid = True

            if valid:
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

        # print("All awards")
        # for merged_award in merged_awards.getKeys():
        #     print(merged_award)

        with open("C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\awards.pkl", 'wb') as file:
            pkl.dump(merged_awards, file)

        return merged_awards
