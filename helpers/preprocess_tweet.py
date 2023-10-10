# Preprocessing function for English tweets
def preprocess_tweet(tweet):
    # Extract hashtags and mentions
    hashtags = [word.lower() for word in tweet['text'].split() if word.startswith('#')]
    mentions = [word.lower() for word in tweet['text'].split() if word.startswith('@')]

    # Remove mentions and hashtags from the text
    text = tweet['text']
    for element in mentions + hashtags:
        text = text.replace(element, '')

    # Tokenization with NLTK, keeping special cases together
    tokens = []
    current_token = ""
    for char in text:
        if char.isalnum() or char in ["'", "_"]:
            current_token += char
        elif char in ["@", "#"] and current_token == "":
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if not char.isspace():
                tokens.append(char)

    if current_token:
        tokens.append(current_token)

    # Check if it's a retweet
    is_retweet = tweet['text'].startswith("RT ")

    # Update the tweet dictionary with extracted information
    tweet['tokens'] = tokens
    tweet['hashtags'] = hashtags
    tweet['mentions'] = mentions
    tweet['is_retweet'] = is_retweet
