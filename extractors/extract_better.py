import re
from utils.regex import NAME_REGEX, MOVIE_REGEX
from data_structures.SortedDict import SortedDict

# filter_tweets: [Tweets()] str str [str] [str] -> [""]
# Get all Tweets with mentions for a single award
def filter_tweets(tweets, filter_regex):
    relevant_tweets = []

    for tweet in tweets:
        filter_result = filter_regex.search(tweet.get_original_text())
        if filter_result:
            relevant_tweets.append(filter_result.group())

    return list(set(relevant_tweets))


# correct_spelling: str [str] [str] -> str [str] [str]
# Double check spellings of currently-picked winners, nominees, presenters
def correct_spelling(winner, nominees, presenters):
    pass

# Get more winners
def extract_more_winners(filtered_tweets, award, nominees, presenters):
    winners = SortedDict()

    for tweet in filtered_tweets:
        # Associated with award
        matches = re.findall(FILM_REGEX, tweet.replace(award.lower(), ' '))

        # Associated with a nominee
        for nominee in nominees:
            if nominee in tweet:
                matches.extend(re.findall(FILM_REGEX, tweet.replace(nominee, ' ')))

        # Associated with a presenter
        for presenter in presenters:
            if presenter in tweet:
                matches.extend(re.findall(FILM_REGEX, tweet.replace(presenter, ' ')))

     # Iterate through each match and update the winner dictionary.
    for match in matches:
        if match in winners:
            winners[match] += 1
        else:
            # Exclude unwanted matches.
            if match == 'RT' or match == 'GoldenGlobes' or match == 'Golden Globes':
                continue
            winners[match] = 1

    print("AWARD", award, "WINNER", winners.getTop(1))
    return winners.getTop(1)

# Get more nominees
def extract_more_nominees(filtered_tweets, award, winner, nominees, presenters):
    more_nominees = SortedDict()

    for tweet in filtered_tweets:
        # Associated with award
        matches = re.findall(FILM_REGEX, tweet.replace(award.lower(), ' '))

        if winner and winner in tweet:
            matches.extend(re.findall(FILM_REGEX, tweet.replace(award.lower(), ' ')))

        # Associated with a nominee
        for nominee in nominees:
            if nominee in tweet:
                matches.extend(re.findall(FILM_REGEX, tweet.replace(nominee, ' ')))

        # Associated with a presenter
        for presenter in presenters:
            if presenter in tweet:
                matches.extend(re.findall(FILM_REGEX, tweet.replace(presenter, ' ')))

     # Iterate through each match and update the winner dictionary.
    for match in matches:
        if match in more_nominees:
            more_nominees[match] += 1
        else:
            # Exclude unwanted matches.
            if match == 'RT' or match == 'GoldenGlobes' or match == 'Golden Globes':
                continue
            more_nominees[match] = 1

    print("AWARD", award, "NOMINEES", more_nominees.getTop(5))
    return more_nominees.getTop(5)

# Get more presenters
def extract_more_presenters(filtered_tweets, award, winner, nominees, presenters):
    pass

# Use our first round of extraction to inform a second round
def extract_more_info(tweets, awards):
    # Extract corresponding information for each award
    print("EXTRACTING INFO FROM AWARDS...")
    award_names = [a.get_name() for a in awards] # [""]
    winner_names = [a.get_winner() for a in awards] # [""]
    nominees_names = [a.get_nominees() for a in awards] # [""]
    presenters_names = [a.get_presenters() for a in awards] # [""]

    # FOOLPROOF GET PEOPLE AND AWARDS
    congrats_regex = re.compile(f'Congrats to {NAME_REGEX} for .* - {MOVIE_REGEX}(?![http|#])')
    relevant_tweets = filter_tweets(tweets, congrats_regex)
    print(relevant_tweets)

    exit(0)







    for i in range(len(award_names)):
        # Get corresponding information for currently-indexed award
        award_i = award_names[i]
        winner_i = winner_names[i]
        nominees_i = nominees_names[i]
        presenters_i = presenters_names[i]

        

        # Get winners if award doesn't have one
        more_winner_i = extract_more_winners(relevant_tweets, award_i, nominees_i, presenters_i)

        # Get more nominees for each award
        # more_nominees_i = extract_more_nominees(relevant_tweets, award_i, winner_i, nominees_i, presenters_i)

        print()

        # Get more presenters for each award
        # more_presenters_i = extract_more_presenters(relevant_tweets, award_i, winner_i, nominees_i, presenters_i)

        # Correct spelling for each item in our awards_ceremony based on database
