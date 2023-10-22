import re
import datetime
from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher

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

#Run award regex on tweet text, if match:
    #Look through the context to see if any secondary validation regexes pass
    #If they pass add the regex to the direction with a vote of 1
    #If we find any awards that look similar to our current regex, add vote to that one and dont add new regex
    #(Consider those the same award, threshold for similarity is about 70%)

def get_similarity_ratio(text1, text2):
    text1 = text1.lower()
    text2 = text2.lower()
    return SequenceMatcher(None, text1, text2).ratio()

def extract_award_names(tweets):

    #r'#(?i)(?:best)[A-Z][a-zA-Z\s]+' Hashtag regex (?), #...(award) might work for cecil
    unprocessed_awards = []
    processed_awards = SortedDict()

    #Didn't get the Best Motion Picture nor Best Performation by Actor/Actress, nor cecil award
    award_regex = r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?'

    validation_regexes = [r'(?:won|wins|winning|takes home|takes|gets|got|getting) (?:the\s)?(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)?', #Wins Regex (Award Object)                             # Win regex, e.g. "X won Y award", "X wins Y award"
                          r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)? (?:goes to|is awarded to)']  #Wins Regex (Award Subject)

    #Regex Validation
    for tweet in tweets:
        #Find instance of potential award mentioning
        regex_matches = re.findall(award_regex, tweet.get_original_text())

        #If there was a mention
        if regex_matches:
            #Do context matching
            for validation_regex in validation_regexes:
                #If context matching succeeds, add to a bucket of each award occurance
                if re.search(validation_regex, tweet.get_original_text(), re.IGNORECASE):
                    for match in regex_matches:
                        unprocessed_awards.append(match)

    for unprocessed_award in unprocessed_awards:
        merged = False

        for key in processed_awards.getKeys():
            if get_similarity_ratio(unprocessed_award, key) >= 0.65:
                processed_awards.updateKV_Pair(key, processed_awards.get(key)+1)
                merged = True
                break
        if not merged:
            processed_awards.add(unprocessed_award, 1)

    print(processed_awards.getTop(30))


#Uses timestamps for validation of nominee status for particular award
def extract_nominees (tweet):
    nominee_regex = r''

    validation_regex = [r'',
                        r'',
                        r'']