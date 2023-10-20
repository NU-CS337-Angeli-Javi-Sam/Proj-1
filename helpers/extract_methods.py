import re
import datetime

def extract_award_names(tweets):
    # Regex for the hashtag awards:  #(?i)(?:best) [A-Z][a-zA-Z\s]+
    unprocessed_award_names = []
    award_references = ["best screenplay - motion picture", "best director - motion picture", "best performance by an actress in a television series - comedy or musical",
                        "best foreign language film", "best performance by an actor in a supporting role in a motion picture",
                        "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
                        "best motion picture - comedy or musical", "best performance by an actress in a motion picture - comedy or musical",
                        "best mini-series or motion picture made for television", "best original score - motion picture", "best performance by an actress in a television series - drama",
                        "best performance by an actress in a motion picture - drama", "cecil b. demille award", "best performance by an actor in a motion picture - comedy or musical",
                        "best motion picture - drama", "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television",
                        "best performance by an actress in a supporting role in a motion picture", "best television series - drama",
                        "best performance by an actor in a mini-series or motion picture made for television", "best performance by an actress in a mini-series or motion picture made for television",
                        "best animated feature film", "best original song - motion picture", "best performance by an actor in a motion picture - drama",
                        "best television series - comedy or musical", "best performance by an actor in a television series - drama",
                        "best performance by an actor in a television series - comedy or musical", ]

    #Didn't get the Best Motion Picture nor Best Performation by Actor/Actress, nor cecil award
    award_regex = r'(?i)(?:best) [A-Z][a-zA-Z\s]+(?:award)'

    for tweet in tweets:
        regex_matches = re.findall(award_regex, tweet.get_original_text())

        if regex_matches:
            for match in regex_matches:
                unprocessed_award_names.append([tweet.get_timestamp(), match])

    award_names = []
    threshold = 0.30

    for award_name in unprocessed_award_names:
        time, award = award_name

        award = award.lower()

        for reference in award_references:
            reference = reference.lower()

            award_set = set(award.split())
            ref_set = set(reference.split())

            intersection_size = len(ref_set.intersection(award_set))
            union_size = len(award_set) + len(ref_set) - intersection_size

            similarity_score = intersection_size / union_size

            if similarity_score >= threshold:
                award_names.append((time, award))

    sorted_award_names = sorted(award_names, key=lambda x: x[0])
    award_names_set = set(sorted_award_names)

    for award in award_names_set:
        print(award)
    print(len(award_names_set))

def extract_nominees (tweet):
    pass