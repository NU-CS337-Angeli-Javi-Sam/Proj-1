from data_structures.SortedDict import SortedDict


class TweetHistogram:
    """
    Represents a word frequency histogram of all tokens extracted from a collection of tweets within a time slice.

    This class provides functionality to collect tokens from tweets, calculate word frequencies, and maintain a word cloud.
    The word cloud is a SortedDict where keys are tokens, and values are their frequencies.

    Attributes:
    - tokenHeap (list): A list to store tokens extracted from tweets.
    - wordCloud (SortedDict): A SortedDict to store tokens and their corresponding frequencies.

    Methods:
    - getWordCloud: Get the word cloud as a SortedDict.
    - addTweet: Add tokens from a tweet to the token heap.
    - createWordCloud: Calculate and create the word cloud based on token frequencies.
    - __str__: Get a string representation of the word cloud.

    """

    def __init__(self):
        """
        Initializes a TweetHistogram object with an empty token heap and word cloud.
        """

        self.__tokenHeap = []
        self.__wordCloud = SortedDict()

    def getWordCloud(self):
        """
        Get the word cloud as a SortedDict.

        Returns:
        - SortedDict: A SortedDict containing tokens and their frequencies.
        """

        return self.__wordCloud

    def addTweet(self, tweet):
        """
        Add tokens from a tweet to the token heap.

        Parameters:
        - tweet (Tweet): A Tweet object containing tokens to be added to the token heap.
        """

        for token in tweet.get_tokens():
            self.__tokenHeap.append(token)

    def createWordCloud(self):
        """
        Calculate and create the word cloud based on token frequencies.
        """

        for token in self.__tokenHeap:
            if token in self.__wordCloud:
                self.__wordCloud.updateKV_Pair(token, self.__wordCloud.get(token) + 1)
            else:
                self.__wordCloud.add(token, 1)

    def __str__(self):
        """
        Get a string representation of the word cloud.

        Returns:
        - str: A formatted string representation of the word cloud.
        """

        return self.__wordCloud.__str__()
