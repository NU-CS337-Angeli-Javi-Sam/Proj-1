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

  def __str__(self):
    output =f"tweet_id: {self.get_tweet_id()}\n"
    output += f"tweet_username: {self.get_username()}\n"
    output += f"tweet_user_id: {self.get_user_id()}\n"
    output += f"tweet_timestamp: {self.get_timestamp()}\n"
    output += f"twee_text: {self.get_original_text()}\n"
    output += f"tweet_tokens: {self.get_tokens()}\n"
    output += f"tweet_mentions: {self.get_mentions()}\n"
    output += f"tweet_hashtags: {self.get_hashtags()}\n"
    output += f"Is it a retweet? {self.is_retweet()}\n"

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
