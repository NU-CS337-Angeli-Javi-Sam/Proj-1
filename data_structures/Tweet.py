import re


class Tweet:
  def __init__(self, data):
    self.__id = data['id']
    self.__text = data['text']
    self.__timestamp_ms = data['timestamp_ms']
    self.__username = data['user']['screen_name']
    self.__user_id = data['user']['id']
    self.__tokens = self.__tokenize__(data['text'])
    self.__hashtags = [word.lower() for word in data['text'].split() if word.startswith('#')]
    self.__mentions = [word.lower() for word in data['text'].split() if word.startswith('@')]
    self.__is_retweet  = data['text'].startswith("RT ")
    self.__has_emojis = self.__identify_emojis__(data['text'])
    # self.__language = self.__identify_language(data['text'])

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

    return tokens

  def __identify_emojis__(self, text):
    # Your existing pattern to match emojis using Unicode escape sequences
    emoji_unicode_pattern = re.compile(r'\\u[0-9a-fA-F]{4}', re.UNICODE)

    # Pattern to match actual emojis (Unicode code points)
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001F004-\U0001F0CF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]+', re.UNICODE)

    # Combine the patterns to match both Unicode escape sequences and actual emojis
    combined_emoji_pattern = re.compile(f'{emoji_unicode_pattern.pattern}|{emoji_pattern.pattern}', re.UNICODE)

    return bool(combined_emoji_pattern.search(text))

  def __str__(self):
    output =f"tweet_id: {self.get_tweet_id()}\n"
    output += f"tweet_username: {self.get_username()}\n"
    output += f"tweet_user_id: {self.get_user_id()}\n"
    output += f"tweet_timestamp: {self.get_timestamp()}\n"
    output += f"tweet_text: {self.get_original_text()}\n"
    output += f"tweet_tokens: {self.get_tokens()}\n"
    output += f"tweet_mentions: {self.get_mentions()}\n"
    output += f"tweet_hashtags: {self.get_hashtags()}\n"
    output += f"Is it a retweet? {self.is_retweet()}\n"
    output += f"Does it have emojis? {self.has_emojis()}\n"
    # output += f"tweet_language {self.has_emojis()}\n"

    return output

  def get_original_text(self):
    return self.__text

  def get_tweet_id(self):
    return self.__id

  def get_timestamp(self):
    return self.__timestamp_ms

  def get_username(self):
    return self.__username

  def get_user_id(self):
    return self.__user_id

  def get_tokens(self):
    return self.__tokens

  def get_hashtags(self):
    return self.__hashtags

  def get_mentions(self):
    return self.__mentions

  def is_retweet(self):
    return self.__is_retweet

  def has_emojis(self):
    return self.__has_emojis

  # def get_language(self):
  #   return self.__language
