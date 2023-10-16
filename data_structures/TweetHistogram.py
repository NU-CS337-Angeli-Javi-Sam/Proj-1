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

        def createWordCloud(self):
            for token in self.__tokenHeap:
                if token in self.__wordCloud:
                    self.__wordCloud.updateKV_Pair(token, self.__wordCloud.get(token) + 1)
                else:
                    self.__wordCloud.add(token, 1)

        def __str__(self):
            return self.__wordCloud.__str__()