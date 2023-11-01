import re
from data_structures.SortedDict import SortedDict
from utils.keywords import PERSON_KEYWORDS
from utils.regex import NOMINEES_REGEX

def extract_nominees(tweets, awards_winners_list):

    # Remove awards that don't have winners
    existing_awards_winners = {}
    for k, v in awards_winners_list.items():
        if v:
            existing_awards_winners[k] = v

    # Map award names to nominees
    awards_nominees = {}

    # Get award names
    awards = existing_awards_winners.keys()

    for award in awards:
        # Get top winner for each award
        top_winner = existing_awards_winners[award].getTop(1)[0][0]

        awards_nominees[award] = SortedDict()

        for regex in NOMINEES_REGEX:
            # Customize regex for each winner
            if "{Winner}" in regex:
                regex = regex.replace('{Winner}', top_winner)

            for tweet in tweets:
                # Check if award is for a person
                if len(list(set(award.split(" ")) & set(PERSON_KEYWORDS))) > 0:
                    matches = re.findall(regex, tweet.get_original_text())
                    for match in matches:
                        if match in awards_nominees[award].getKeys():
                            awards_nominees[award][match] += 1
                        elif "Golden" not in match:
                            awards_nominees[award][match] = 1



    return awards_nominees
