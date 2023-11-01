from data_structures.SortedDict import SortedDict
from data_structures.TweetHistogram import TweetHistogram

class TweetStats:

    def __init__(self, duration = 60000):
        self.__histograms = {}
        self.__retweets = {}
        self.__topRetweeted = SortedDict()
        self.__topMentioned = SortedDict()
        self.__topHashtags = SortedDict()
        self.__topTweeters = SortedDict()

        self.__tweetLog = []

        self.__k = 10

        self.__timeslice_start = None
        self.__timeslice_duration = duration
        self.__timeslice_end = None

    def setK (self, k):
        self.__k = k

    def getK (self):
        return self.__k

    def getHistograms (self):
        return self.__histograms

    def getRetweets (self):
        return self.__retweets

    def getTopRetweeted (self):
        return self.__topRetweeted

    def getTopMentioned (self):
        return self.__topMentioned

    def getTopHashTags (self):
        return self.__topHashtags

    def getTopTweeters(self):
        return self.__topTweeters


    def logTweet (self, tweet):

        if not self.__timeslice_start:
            self.__timeslice_start = tweet.get_timestamp()

            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()


        while self.__timeslice_end < tweet.get_timestamp():
            self.__timeslice_start = self.__timeslice_end

            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()

        for k, v in self.__histograms.items():
            if k[0] <= tweet.get_timestamp() < k[1]:
                v.addTweet(tweet)

        self.__tweetLog.append(tweet)


    def analyzeTweets(self):
        # print("Creating Word Clouds")
        # # Creates Word clouds for histograms
        # for v in self.__histograms.values():
        #     v.createWordCloud()
        # print("Finished Word Clouds")

        for tweet in self.__tweetLog:
            username = tweet.get_username()
            if username not in self.__topTweeters:
                self.__topTweeters.add(username, 1)
            else:
                self.__topTweeters.updateKV_Pair(username, self.__topTweeters.get(username) + 1)

            hashtags = tweet.get_hashtags()

            if hashtags:
                for hashtag in hashtags:
                    if hashtag not in self.__topHashtags:
                        self.__topHashtags.add(hashtag, 1)
                    else:
                        self.__topHashtags.updateKV_Pair(hashtag, self.__topHashtags.get(hashtag) + 1)

            mentions = tweet.get_mentions()

            if mentions:
                for mention in mentions:
                    if mention not in self.__topMentioned:
                        self.__topMentioned.add(mention, 1)
                    else:
                        self.__topMentioned.updateKV_Pair(mention, self.__topMentioned.get(mention) + 1)

            if tweet.is_retweet() and mentions:
                retweeted_acc = mentions[0]
                original_text = tweet.get_original_text()

                rt_index = original_text.find("RT ")
                retweeted_text = original_text[rt_index + len("RT " + retweeted_acc + " "):]

                if retweeted_acc not in self.__retweets:
                    self.__retweets[retweeted_acc] = []
                    self.__retweets[retweeted_acc].append(retweeted_text)
                else:
                    if retweeted_text not in self.__retweets[retweeted_acc]:
                        self.__retweets[retweeted_acc].append(retweeted_text)

                if retweeted_acc not in self.__topRetweeted:
                    self.__topRetweeted.add(retweeted_acc, 1)
                else:
                    self.__topRetweeted.updateKV_Pair(retweeted_acc, self.__topRetweeted.get(retweeted_acc) + 1)

    def optimize(self):
        pass

    def __str__(self):
        output = "TweetStats: \n\n"

        # output += "Histograms:\n"
        # for key, value in self.__histograms.items():
        #     output += f"{key}: {value}\n"

        output += "Top Retweeted:\n"
        output += str(self.__topRetweeted.getTop(self.__k))
        output += '\n'

        output += "Retweets:\n"
        retweeted_accs = self.__topRetweeted.getSortedKeys()[0:self.__k]
        for key, value in self.__retweets.items():
            if key in retweeted_accs:
                output += f"\t{key}: {value}\n"

        output += "Top Mentioned:\n"
        output += str(self.__topMentioned.getTop(self.__k))
        output += '\n'

        output += "Top Hashtags:\n"
        output += str(self.__topHashtags.getTop(self.__k))
        output += '\n'

        output += "Top Tweeters:\n"
        output += str(self.__topTweeters.getTop(self.__k))
        output += '\n'

        return output
