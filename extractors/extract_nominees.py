import re
import pickle as pkl

def extract_nominees(tweets):

    awards_winners_list = None

    with open("C:\\Users\\samj9\\PycharmProjects\\Proj-1\\extractors\\award_winners.pkl", "rb") as file:
        awards_winners_list = pkl.load(file)

    # awards = awards_winners_list.keys()
    awards = ['Best Director']
    nominee_regexes = [r'({Winner}.*nomin.*([A-Z][a-zA-Z/s]*)+)|(([A-Z][a-zA-Z/s]*)+.*nomin.*{Winner})',
                       r'{Winner}.*over.*([A-Z][a-zA-Z/s]*)+',
                       r'{Winner}.*beat.*([A-Z][a-zA-Z/s]*)+[!#]']

    for award_name in awards:
        print(award_name)
        for winner_name in awards_winners_list[award_name].getSortedKeys():
            print(winner_name)
            for tweet in tweets:
                regex_matches = []

                # Find all the matches to our regexes for this particular tweet
                for nominee_regex in nominee_regexes:
                    temp_nom_regex = nominee_regex.replace('{Winner}', winner_name)

                    matches = re.findall(temp_nom_regex, tweet.get_original_text())

                    regex_matches.extend(matches)

                for regex_match in regex_matches:
                    print(regex_match)

