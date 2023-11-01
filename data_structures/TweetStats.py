from data_structures.SortedDict import SortedDict
from data_structures.TweetHistogram import TweetHistogram

class TweetStats:
    """
    A class for collecting and managing statistics related to tweets, including histograms, retweets, and top lists.

    Attributes:
    - histograms (dict): A dictionary of TweetHistogram objects for different time slices.
    - retweets (dict): A dictionary containing retweet counts for each tweet.
    - topRetweeted (SortedDict): A sorted dictionary of tweets sorted by the number of retweets.
    - topMentioned (SortedDict): A sorted dictionary of Twitter users mentioned the most in tweets.
    - topHashtags (SortedDict): A sorted dictionary of the most used hashtags in tweets.
    - topTweeters (SortedDict): A sorted dictionary of Twitter users with the most tweets.
    - tweetLog (list): A list to store tweet objects.
    - k (int): The value for controlling the number of top items to retrieve.
    - timeslice_start (int): The start time of the current time slice.
    - timeslice_duration (int): The duration of each time slice in milliseconds.
    - timeslice_end (int): The end time of the current time slice.
    """

    def __init__(self, duration = 60000):
        """
        Initializes a TweetStats object with the given time slice duration.

        Parameters:
        - duration (int): The duration of each time slice in milliseconds.
        """
        self.__histograms = {}  # A dictionary of TweetHistogram objects for different time slices.
        self.__retweets = {}  # A dictionary containing retweet counts for each tweet.
        self.__topRetweeted = SortedDict()  # A sorted dictionary of tweets sorted by the number of retweets.
        self.__topMentioned = SortedDict()  # A sorted dictionary of the most mentioned Twitter users.
        self.__topHashtags = SortedDict()  # A sorted dictionary of the most used hashtags in tweets.
        self.__topTweeters = SortedDict()  # A sorted dictionary of Twitter users with the most tweets.
        self.__tweetLog = []  # A list to store tweet objects.
        self.__k = 10  # The value for controlling the number of top items to retrieve.
        self.__timeslice_start = None  # The start time of the current time slice.
        self.__timeslice_duration = duration  # The duration of each time slice in milliseconds.
        self.__timeslice_end = None  # The end time of the current time slice.

    def setK(self, k):
        """
        Set the value of k to control the number of top items to retrieve.

        Parameters:
        - k (int): The value for controlling the number of top items to retrieve.
        """
        self.__k = k

    def getK(self):
        """
        Get the current value of k.

        Returns:
        - int: The current value of k.
        """
        return self.__k

    def getHistograms(self):
        """
        Get the TweetHistogram objects for different time slices.

        Returns:
        - dict: A dictionary of TweetHistogram objects.
        """
        return self.__histograms

    def getRetweets(self):
        """
        Get the dictionary of retweet counts for each tweet.

        Returns:
        - dict: A dictionary containing retweet counts for each tweet.
        """
        return self.__retweets

    def getTopRetweeted(self):
        """
        Get a sorted dictionary of tweets sorted by the number of retweets.

        Returns:
        - SortedDict: A sorted dictionary of tweets.
        """
        return self.__topRetweeted

    def getTopMentioned(self):
        """
        Get a sorted dictionary of the most mentioned Twitter users.

        Returns:
        - SortedDict: A sorted dictionary of Twitter users.
        """
        return self.__topMentioned

    def getTopHashtags(self):
        """
        Get a sorted dictionary of the most used hashtags in tweets.

        Returns:
        - SortedDict: A sorted dictionary of hashtags.
        """
        return self.__topHashtags

    def getTopTweeters(self):
        """
        Get a sorted dictionary of Twitter users with the most tweets.

        Returns:
        - SortedDict: A sorted dictionary of Twitter users.
        """
        return self.__topTweeters

    def logTweet(self, tweet):
        """
        Log a tweet and update the associated TweetHistogram within the defined time slices.

        This method logs a tweet, associates it with the corresponding time slice, and updates the TweetHistogram object
        for that time slice. If the tweet's timestamp falls outside of existing time slices, new time slices are created.

        Parameters:
        - tweet (Tweet): The tweet object to be logged.

        Returns:
        - None
        """
        if not self.__timeslice_start:
            # If the time slice is not set, initialize it based on the tweet's timestamp.
            self.__timeslice_start = tweet.get_timestamp()
            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()

        while self.__timeslice_end < tweet.get_timestamp():
            # If the tweet's timestamp exceeds the current time slice, create a new time slice.
            self.__timeslice_start = self.__timeslice_end
            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()

        for k, v in self.__histograms.items():
            # Associate the tweet with the appropriate time slice and update the corresponding TweetHistogram.
            if k[0] <= tweet.get_timestamp() < k[1]:
                v.addTweet(tweet)

        self.__tweetLog.append(tweet)

    def analyzeTweets(self):
        """
        Analyze the tweets and update tweet statistics.

        This method processes the tweets in the `tweetLog` of the `TweetStats` object. It analyzes each tweet to update
        various tweet statistics including top tweeters, top hashtags, top mentioned accounts, retweets, and top retweeted
        accounts. It also creates word clouds for the tweet histograms (not currently enabled, commented out in the code).

        The method iterates through each tweet and updates the statistics based on the tweet's content, mentions, hashtags,
        and whether it's a retweet.

        Returns:
        - None: This method updates the internal tweet statistics but doesn't return a value.
        """
        # print("Creating Word Clouds")
        # # Creates Word clouds for histograms
        # for v in self.__histograms.values():
        #     v.createWordCloud()
        # print("Finished Word Clouds")

        # Iterate through each tweet in the tweetLog
        for tweet in self.__tweetLog:
            # Get the username of the tweet's author
            username = tweet.get_username()

            # Update the top tweeters statistics
            if username not in self.__topTweeters:
                self.__topTweeters.add(username, 1)
            else:
                self.__topTweeters.updateKV_Pair(username, self.__topTweeters.get(username) + 1)

            # Get the list of hashtags in the tweet
            hashtags = tweet.get_hashtags()

            if hashtags:
                # Iterate through hashtags and update top hashtags statistics
                for hashtag in hashtags:
                    if hashtag not in self.__topHashtags:
                        self.__topHashtags.add(hashtag, 1)
                    else:
                        self.__topHashtags.updateKV_Pair(hashtag, self.__topHashtags.get(hashtag) + 1)

            # Get the list of mentioned accounts in the tweet
            mentions = tweet.get_mentions()

            if mentions:
                # Iterate through mentions and update top mentioned accounts statistics
                for mention in mentions:
                    if mention not in self.__topMentioned:
                        self.__topMentioned.add(mention, 1)
                    else:
                        self.__topMentioned.updateKV_Pair(mention, self.__topMentioned.get(mention) + 1)

            # Check if the tweet is a retweet and if there are mentions
            if tweet.is_retweet() and mentions:
                # Get the username of the retweeted account
                retweeted_acc = mentions[0]

                # Get the original text of the retweet
                original_text = tweet.get_original_text()

                # Find the index of "RT" in the retweet
                rt_index = original_text.find("RT ")

                # Extract the retweeted text
                retweeted_text = original_text[rt_index + len("RT " + retweeted_acc + " "):]

                # Update retweets dictionary with the retweeted account and text
                if retweeted_acc not in self.__retweets:
                    self.__retweets[retweeted_acc] = []
                    self.__retweets[retweeted_acc].append(retweeted_text)
                else:
                    if retweeted_text not in self.__retweets[retweeted_acc]:
                        self.__retweets[retweeted_acc].append(retweeted_text)

                # Update the top retweeted accounts statistics
                if retweeted_acc not in self.__topRetweeted:
                    self.__topRetweeted.add(retweeted_acc, 1)
                else:
                    self.__topRetweeted.updateKV_Pair(retweeted_acc, self.__topRetweeted.get(retweeted_acc) + 1)

    def __str__(self):
        """
        Return a formatted string representation of TweetStats.

        This method constructs and returns a string that represents the TweetStats object. It includes information about the
        top retweeted accounts, retweet counts, top mentioned accounts, top hashtags, and top tweeters.

        Returns:
        - str: A formatted string representation of TweetStats, including top retweeted accounts, retweet counts, top mentioned
        accounts, top hashtags, and top tweeters.
        """
        output = "TweetStats: \n\n"

        # output += "Histograms:\n"
        # for key, value in self.__histograms.items():
        #     output += f"{key}: {value}\n"

        output += "Top Retweeted:\n"
        output += str(self.__topRetweeted.getTop(self.__k))
        output += '\n\n'

        output += "Retweets:\n"
        retweeted_accs = self.__topRetweeted.getSortedKeys()[0:self.__k]
        for key, value in self.__retweets.items():
            if key in retweeted_accs:
                output += f"\t{key}: {value[:5]}\n\n"

        output += "Top Mentioned:\n"
        output += str(self.__topMentioned.getTop(self.__k))
        output += '\n\n'

        output += "Top Hashtags:\n"
        output += str(self.__topHashtags.getTop(self.__k))
        output += '\n\n'

        output += "Top Tweeters:\n"
        output += str(self.__topTweeters.getTop(self.__k))
        output += '\n'

        return output
