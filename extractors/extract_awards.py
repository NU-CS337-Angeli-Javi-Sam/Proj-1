from data_structures.SortedDict import SortedDict
from difflib import SequenceMatcher
import re
from utils.keywords import AWARDS_KEYWORDS, TRASH_KEYWORDS, MINOR_KEYWORDS
from utils.regex import AWARDS_REGEX, AWARDS_VALIDATION_REGEX

"""
Extract awards method
    Given: Tweet Objects
    Returns: SortDict of Award_names to Confidence Vote
"""

# Gets the similarity ratio between 2 strings
def get_similarity_ratio(text1, text2, words):
    """
    Calculate the similarity ratio between two texts after removing specified words.

    This function calculates the similarity ratio between two input texts after converting them to lowercase and removing
    specific words provided in the 'words' list.

    Parameters:
    - text1 (str): The first input text.
    - text2 (str): The second input text.
    - words (list of str): A list of words to be removed from both texts.

    Returns:
    - float: The similarity ratio between the two texts.
    """

    # Convert texts to lowercase
    text1 = text1.lower()
    text2 = text2.lower()

    # Remove specified words from both texts
    text1 = replace_words(text1, words, " ")
    text2 = replace_words(text2, words, " ")

    # Calculate and return the similarity ratio using SequenceMatcher
    return SequenceMatcher(None, text1, text2).ratio()

def replace_words(text, words, replacement):
    """
    Remove specified words from a text and replace them with a given replacement.

    This function removes specific words from a text and replaces them with a specified replacement string.

    Parameters:
    - text (str): The input text from which words will be removed.
    - words (list of str): A list of words to be removed.
    - replacement (str): The replacement string for removed words.

    Returns:
    - str: The modified text with specified words replaced.
    """

    for word in words:
        if word in text.lower():
            # Replace the word with the specified replacement
            text.lower().replace(word, replacement)
    return text

def remove_endphrase(text, words):
    """
    Remove phrases in the text that end with specified words.

    This function removes phrases in the input text that end with specified words found in the 'words' list.

    Parameters:
    - text (str): The input text from which phrases will be removed.
    - words (list of str): A list of words that mark the end of phrases to be removed.

    Returns:
    - str: The modified text with phrases removed.
    """

    for word in words:
        if word in text.lower():
            # Find the position of the last occurrence of the specified word and remove the phrase beyond it
            text = text[: text.lower().find(word)]
    return text

def extract_awards(tweets):
    """
    Extract potential award mentions from a list of tweets and filter them based on context and keywords.

    This function analyzes a list of tweets to identify potential award mentions using a set of regular expressions.
    It then filters and consolidates these mentions based on context and predefined keywords.

    Parameters:
    - tweets (list of Tweet): A list of Tweet objects containing tweet text.

    Returns:
    - SortedDict: A SortedDict object containing identified award mentions as keys and their frequencies as values.
    """
    # A list to store unmerged potential award mentions
    unmerged_awards = []

    # A SortedDict to store merged and validated award mentions
    merged_awards = SortedDict()

    # Go through each award
    for tweet in tweets:

        # A list to store matches found in the tweet
        regex_matches = []

        # Find instances of potential award mentions using multiple award-related regex patterns
        for award_regex in AWARDS_REGEX:
            matches = re.findall(award_regex, tweet.get_original_text())
            regex_matches.extend(matches)

        # If there were any matches, proceed with context matching
        if regex_matches:
            for validation_regex in AWARDS_VALIDATION_REGEX:

                # Check if the tweet's text context matches the validation regex
                if re.search(validation_regex, tweet.get_original_text()):
                    for match in regex_matches:
                        match = remove_endphrase(match, TRASH_KEYWORDS)

                        temp_match = replace_words(match, MINOR_KEYWORDS, " ")

                        # Check if the potential award mention is in title case
                        if temp_match.istitle():
                            unmerged_awards.insert(0, match)
                        else:
                            unmerged_awards.append(match)

    # Merge similar awards based on context and keywords
    for unmerged_award in unmerged_awards:
        valid = False

        for keyword in AWARDS_KEYWORDS:
            if keyword in unmerged_award.lower():
                valid = True

        if valid:
            merged = False

            # Iterate through the merged_awards dictionary
            for key in merged_awards.getKeys():

                # Calculate the similarity ratio between the unmerged award and existing awards
                if get_similarity_ratio(unmerged_award, key, MINOR_KEYWORDS) >= 0.67:
                    # Update the count of the matched award
                    merged_awards.updateKV_Pair(key, merged_awards.get(key) + 1)
                    merged = True
                    break
            if not merged:
                merged_awards.add(unmerged_award, 1)

    final_awards = SortedDict()

    # Filter awards with more than one instance and store them in final_awards
    for key, value in merged_awards.getItems():
        if value > 2:
            final_awards[key] = value

    return final_awards
