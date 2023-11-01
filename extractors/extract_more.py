import re
from utils.regex import NAME_REGEX, NAME_SLASH_REGEX, NAME_HASHTAG_REGEX

# filter_tweets: [Tweets()] str str [str] [str] -> [Tweets()]
# Get all Tweets with mentions for a single award
def filter_tweets(tweets, award, winner, nominees, presenters):
    relevant_tweets = []
    items_for_filtering = [award] + [winner] + nominees + presenters

    for tweet in tweets:
        for item in items_for_filtering:
            if item in tweet.get_original_text():
                relevant_tweets.append(tweet)

    return list(set(relevant_tweets))


# correct_spelling: str [str] [str] -> str [str] [str]
# Double check spellings of currently-picked winners, nominees, presenters
def correct_spelling(winner, nominees, presenters):
    pass

# Get more winners
def extract_more_winners(filtered_tweets, award, nominees, presenters):
    pass

# Get more nominees
def extract_more_nominees(filtered_tweets, award, winner, nominees, presenters):
    pass

# Get more presenters
def extract_more_presenters(filtered_tweets, award, winner, nominees, presenters):
    pass

# Use our first round of extraction to inform a second round
def extract_more_info(tweets, awards):
    # Extract corresponding information for each award
    print("EXTRACTING INFO FROM AWARDS...")
    award_names = [a.get_name() for a in awards] # [""]
    winner_names = [a.get_winner() for a in awards] # ""
    nominees_names = [a.get_nominees() for a in awards] # [""]
    presenters_names = [a.get_presenters() for a in awards] # [""]

    for i in range(len(award_names)):
        # Get corresponding information for currently-indexed award
        award_i = award_names[i]
        winner_i = winner_names[i]
        nominees_i = nominees_names[i]
        presenters_i = presenters_names[i]

        # Filter tweets to keep those that mention any of the information associated with award_i
        print("GETTING RELEVANT TWEETS....")
        relevant_tweets = filter_tweets(tweets, award_i, winner_i, nominees_i, presenters_i)

        # Get winners if award doesn't have one
        if not winner_i:
            more_winner_i = extract_more_winners(relevant_tweets, award_i, nominees_i, presenters_i)

        # Get more nominees for each award
        more_nominees_i = extract_more_nominees(relevant_tweets, award_i, winner_i, nominees_i, presenters_i)

        # Get more presenters for each award
        more_presenters_i = extract_more_presenters(relevant_tweets, award_i, winner_i, nominees_i, presenters_i)

        # Correct spelling for each item in our awards_ceremony based on database
