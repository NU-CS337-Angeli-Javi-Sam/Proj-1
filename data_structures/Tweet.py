import re
from utils.regex import EMOJI_REGEX, EMOJI_UNICODE_REGEX, NAME_REGEX, TOKENIZER_REGEX


class Tweet:
    """
    Represents a tweet object with various attributes and methods for analyzing tweet content.
    """

    def __init__(self, data):
        """
        Initializes a Tweet object with data from a Twitter API response.

        Parameters:
        - data (dict): A dictionary containing Twitter API response data, including tweet ID,
                       text, timestamp, user information, and more.

        Returns:
        - Tweet: A Tweet object
        """

        self.__id = data["id"]
        self.__text = data["text"]
        self.__timestamp_ms = data["timestamp_ms"]
        self.__username = data["user"]["screen_name"]
        self.__user_id = data["user"]["id"]
        self.__tokens = self.__tokenize__(data["text"])
        self.__hashtags = [
            word.lower() for word in data["text"].split() if word.startswith("#")
        ]
        self.__mentions = [
            word.lower() for word in data["text"].split() if word.startswith("@")
        ]
        self.__is_retweet = data["text"].startswith("RT ")
        self.__has_emojis = self.__identify_emojis__(data["text"])

    def __tokenize__(self, text):
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

        # Find all matches for the name pattern in the text
        name_matches = re.finditer(NAME_REGEX, text)

        # Tokenize the text based on the name matches
        current_position = 0

        for match in name_matches:
            # Tokenize the text before the name
            non_name_text = text[current_position : match.start()]
            non_name_tokens = re.findall(TOKENIZER_REGEX, non_name_text)
            tokens.extend(non_name_tokens)

            # Add the name as a separate token
            name = match.group()
            tokens.append(name)

            # Update the current position
            current_position = match.end()

        # Tokenize any remaining text
        remaining_text = text[current_position:]
        remaining_tokens = re.findall(TOKENIZER_REGEX, remaining_text)
        tokens.extend(remaining_tokens)

        return tokens

    def __identify_emojis__(self, text):
        """
        Identify the presence of emojis in the given text.

        This method uses regular expressions to identify both Unicode emojis and standard emoji patterns in the text.

        Parameters:
        - text (str): The text to be analyzed for emoji presence.

        Returns:
        - bool: True if one or more emojis are found in the text, False otherwise.
        """

        emoji_unicode_pattern = re.compile(EMOJI_UNICODE_REGEX, re.UNICODE)

        emoji_pattern = re.compile(
            EMOJI_REGEX,
            re.UNICODE,
        )

        combined_emoji_pattern = re.compile(
            f"{emoji_unicode_pattern.pattern}|{emoji_pattern.pattern}", re.UNICODE
        )

        return bool(combined_emoji_pattern.search(text))

    def __str__(self):
        """
        Returns a formatted string representation of a Tweet object, including various tweet details.

        Returns:
        - str: A formatted string containing tweet details, such as tweet ID, username, timestamp, text, and more.
        """

        output = f"tweet_id: {self.get_tweet_id()}\n"
        output += f"tweet_username: {self.get_username()}\n"
        output += f"tweet_user_id: {self.get_user_id()}\n"
        output += f"tweet_timestamp: {self.get_timestamp()}\n"
        output += f"tweet_text: {self.get_original_text()}\n"
        output += f"tweet_tokens: {self.get_tokens()}\n"
        output += f"tweet_mentions: {self.get_mentions()}\n"
        output += f"tweet_hashtags: {self.get_hashtags()}\n"
        output += f"Is it a retweet? {self.is_retweet()}\n"
        output += f"Does it have emojis? {self.has_emojis()}\n"

        return output

    def get_original_text(self):
        """
        Get the original text of the tweet.

        Returns:
        - str: The original text of the tweet.
        """

        return self.__text

    def get_tweet_id(self):
        """
        Get the ID of the tweet.

        Returns:
        - int: The unique identifier of the tweet.
        """

        return self.__id

    def get_timestamp(self):
        """
        Get the timestamp of the tweet.

        Returns:
        - str: The timestamp of the tweet in milliseconds.
        """

        return self.__timestamp_ms

    def get_username(self):
        """
        Get the username of the tweet's author.

        Returns:
        - str: The username of the tweet's author.
        """

        return self.__username

    def get_user_id(self):
        """
        Get the user ID of the tweet's author.

        Returns:
        - int: The user ID of the tweet's author.
        """

        return self.__user_id

    def get_tokens(self):
        """
        Get the tokens (words) in the tweet's text.

        Returns:
        - list of str: A list of tokens (words) extracted from the tweet's text.
        """

        return self.__tokens

    def get_hashtags(self):
        """
        Get the hashtags mentioned in the tweet.

        Returns:
        - list of str: A list of hashtags found in the tweet's text.
        """

        return self.__hashtags

    def get_mentions(self):
        """
        Get the user mentions in the tweet.

        Returns:
        - list of str: A list of user mentions found in the tweet's text.
        """

        return self.__mentions

    def is_retweet(self):
        """
        Check if the tweet is a retweet.

        Returns:
        - bool: True if the tweet is a retweet, False otherwise.
        """

        return self.__is_retweet

    def has_emojis(self):
        """
        Check if the tweet contains emojis.

        Returns:
        - bool: True if the tweet contains emojis, False otherwise.
        """

        return self.__has_emojis
