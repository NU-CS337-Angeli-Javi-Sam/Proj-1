class AwardsCeremony:
    """
    Represents an awards ceremony with hosts, awards, and tweet statistics.
    """

    def __init__(self, hosts, awards, tweetstats):
        """
        Initializes an AwardsCeremony object with provided details.

        Parameters:
        - hosts (list of str): List of hosts for the awards ceremony.
        - awards (list of Award): List of Award objects representing award categories.
        - tweetstats (TweetStats): An object containing tweet statistics for the ceremony.

        Returns:
        - AwardsCeremony: An AwardsCeremony object.
        """

        self.__hosts = hosts
        self.__awards = awards
        self.__tweetstats = tweetstats

    def __str__(self):
        """
        Returns a string representation of the AwardsCeremony object.

        Returns:
        - str: A formatted string containing ceremony details including hosts, awards, and tweet statistics.
        """
        output = f"Host: {', '.join(self.get_hosts()).title()}\n\n"
        for award in self.get_awards():
            output += f"{award}\n"

        self.__tweetstats.setK(10)
        output += f"{self.__tweetstats}"

        return output

    def get_hosts(self):
        """
        Get the list of hosts for the awards ceremony.

        Returns:
        - list of str: List of hosts' names.
        """
        return self.__hosts

    def get_awards(self):
        """
        Get the list of awards for the ceremony.

        Returns:
        - list of Award: List of Award objects representing award categories.
        """
        return self.__awards

    def get_tweetstats(self):
        """
        Get the tweet statistics for the awards ceremony.

        Returns:
        - TweetStats: An object containing tweet statistics.
        """
        return self.__tweetstats

    def to_json(self):
        """
        Convert the AwardsCeremony object to a JSON-compatible dictionary.

        Returns:
        - dict: A dictionary containing ceremony details, including hosts, awards, and tweet statistics.
        """
        ceremony_dict = {
            "Host": [host.title() for host in self.get_hosts()],
        }

        for award in self.get_awards():
            ceremony_dict[award.get_name().title()] = award.to_json()

        ceremony_dict["Tweet Stats"] = {
            "Top Mentions": self.__tweetstats.getTopMentioned().getTop(10),
            "Top Retweets": {},
            "Top Hashtags": self.__tweetstats.getTopHashTags().getTop(10),
            "Top Tweeters": self.__tweetstats.getTopTweeters().getTop(10),
        }

        retweeters = self.__tweetstats.getTopRetweeted().getSortedKeys()[0:10]
        retweets = self.__tweetstats.getRetweets()

        for key in retweeters:
            ceremony_dict["Tweet Stats"]["Top Retweets"][key] = retweets[key]

        return ceremony_dict
