from data_structures.SortedDict import SortedDict
from data_structures.TweetHistogram import TweetHistogram


class TweetStats:
    """
    Aggregation of all the tweet metadata
    """
    def __init__(self, duration = 60000):
        #Tuple(Start, End) to Histogram relation
        self.__histograms = {}
        #Retweeted Acc to Retweet
        self.__retweets = {}
        #Retweeted Acc to # Retweets
        self.__topRetweeted = SortedDict()
        #Mentioned Acc to # Mentions
        self.__topMentioned = SortedDict()
        #Hashtag to # Hashtags
        self.__topHashtags = SortedDict()
        #Accounts to # Tweets
        self.__topTweeters = SortedDict()

        self.__timeslice_start = None
        self.__timeslice_duration = duration
        self.__timeslice_end = None

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

    #This function assumes that tweets fed into the tweetStats object chronologically
    def analyzeTweet (self, tweet):
        #If there is no timeslice_start, this must be the first tweet being added
        #Initiate the timeslice markers and the first bucket in the histo dictionary
        if not self.__timeslice_start:
            self.__timeslice_start = tweet.get_timestamp()

            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()

        #Handles if timestamp of current tweet is outside the scope of our final timeslice key
        #Adds a new timeslice bucket until there's one to hold tweet
        while self.__timeslice_end < tweet.get_timestamp():
            self.__timeslice_start = self.__timeslice_end

            self.__timeslice_end = self.__timeslice_start + self.__timeslice_duration
            self.__histograms[(self.__timeslice_start, self.__timeslice_end)] = TweetHistogram()

        for k, v in self.__histograms.items():
            if k[0] <= tweet.get_timestamp() < k[1]:
                v.addTweet(tweet)

        # print(self.__histograms)

        #Updates Top Tweeters
        username = tweet.get_username()
        if username not in self.__topTweeters:
            self.__topTweeters.add(username, 1)
        else:
            self.__topTweeters.updateKV_Pair(username, self.__topTweeters.get(username) + 1)

        # print(self.__topTweeters)

        # Updates Top Hashtags
        hashtags = tweet.get_hashtags()

        if hashtags:
            for hashtag in hashtags:
                if hashtag not in self.__topHashtags:
                    self.__topHashtags.add(hashtag, 1)
                else:
                    self.__topHashtags.updateKV_Pair(hashtag, self.__topHashtags.get(hashtag) + 1)

        # print(self.__topHashtags)

        # Updates Top Mentioned
        mentions = tweet.get_mentions()

        if mentions:
            for mention in mentions:
                if mention not in self.__topMentioned:
                    self.__topMentioned.add(mention, 1)
                else:
                    self.__topMentioned.updateKV_Pair(mention, self.__topMentioned.get(mention) + 1)

        # print(self.__topMentioned)

        #Updates Top Retweeted Accounts and Retweets
        if tweet.is_retweet():
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


    #This function can be used later to clip data that we feel is unnecessary
    #e.g. tweeters who only have 3 tweets or less
    def optimize(self):
        pass

    def __str__(self):
        output = "Tweet Stats: \n\n"

        output += "Histograms:\n"
        for key, value in self.__histograms.items():
            output += f"{key}: {value}\n"

        output += "Retweets:\n"
        for key, value in self.__retweets.items():
            output += f"\t{key}: {value}\n"

        output += "Top Retweeted:\n"
        output += self.__topRetweeted.__str__()
        output += '\n'

        output += "Top Mentioned:\n"
        output += self.__topMentioned.__str__()
        output += '\n'

        output += "Top Hashtags:\n"
        output += self.__topHashtags.__str__()
        output += '\n'

        output += "Top Tweeters:\n"
        output += self.__topTweeters.__str__()
        output += '\n'

        return output



