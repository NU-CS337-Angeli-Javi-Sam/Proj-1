from data_structures.SortedDict import SortedDict

class TweetHistogram:
        """
        Word frequency of all tweets within allocated time slice
        """
        def __init__(self):
            self.__tokenHeap = []
            self.__wordCloud = SortedDict()

        def getWordCloud(self):
            return self.__wordCloud

        def addTweet (self, tweet):
            for token in tweet.get_tokens():
                self.__tokenHeap.append(token)
            self.createWordCloud()

        def createWordCloud(self):
            unique_tokens = set(self.__tokenHeap)
            for token in unique_tokens:
                self.__wordCloud.add(token, self.__tokenHeap.count(token))

        def __str__(self):
            return self.__wordCloud.__str__()