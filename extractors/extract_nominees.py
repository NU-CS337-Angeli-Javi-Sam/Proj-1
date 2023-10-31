import re
from data_structures.SortedDict import SortedDict

person_keywords = [
    "actor",
    "actress",
    "director",
    "writer",
    "producer"
]

bad_words = [
    "Golden",
    "Globes"
]

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

    # print(awards)

    # nominee_regexes = [r'({Winner}.*nomin.*([A-Z][a-zA-Z/s]*)+)|(([A-Z][a-zA-Z/s]*)+.*nomin.*{Winner})']

    for award in awards:
        # Get top winner for each award
        top_winner = existing_awards_winners[award].getTop(1)[0][0]
        # print("AWARD & WINNER: ", award, top_winner)

        awards_nominees[award] = SortedDict()

        # regex = r'{Winner}.* over .*([A-Z][a-z]+ [A-Z][a-z]+)' # WORKS
        regex_lst = [
            # r'({Winner}.*nomin.*([A-Z][a-zA-Z/s]*)+)|(([A-Z][a-zA-Z/s]*)+.*nomin.*{Winner})', # SLOW
            r'{Winner}.* beat .*([A-Z][a-z]+ [A-Z][a-z]+)', # WORKS
            r'{Winner}.* over .*([A-Z][a-z]+ [A-Z][a-z]+)', # WORKS
            # r'hope.*([A-Z][a-z]+ [A-Z][a-z]+)',
            # r'{Winner}.*stole.*([A-Z][a-z]+ [A-Z][a-z]+)', #Bogus Lite
            # r'{Winner}.*rob.*([A-Z][a-z]+ [A-Z][a-z]+)', #Bogus Lite
            r'{Winner}.*snub.*([A-Z][a-z]+ [A-Z][a-z]+)', #C'est Bon
            # r'wish.*([A-Z][a-z]+ [A-Z][a-z]+)',
            r'{Winner}.* [won|win] .*([A-Z][a-z]+ [A-Z][a-z]+)',
            r'{Winner}.*([A-Z][a-z]+ [A-Z][a-z]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+).*{Winner}'
        ]

        for regex in regex_lst:
            # Customize regex for each winner
            if "{Winner}" in regex:
                regex = regex.replace('{Winner}', top_winner)

            for tweet in tweets:
                # Check if award is for a person
                if len(list(set(award.split(" ")) & set(person_keywords))) > 0:
                    matches = re.findall(regex, tweet.get_original_text())
                    for match in matches:
                        if match in awards_nominees[award].getKeys():
                            awards_nominees[award][match] += 1
                        elif "Golden" not in match:
                            awards_nominees[award][match] = 1



    return awards_nominees
