import os
import json
import sys

from data_structures.Award import Award
from data_structures.AwardsCeremony import AwardsCeremony
from data_structures.Tweet import Tweet
from data_structures.TweetStats import TweetStats

from helpers.awards import get_awards_list
from helpers.hosts import get_hosts_list
from helpers.nominees import get_nominees_dict
from helpers.presenters import get_presenters_dict
from helpers.winner import get_winners_dict

from extractors.extract_winners import extract_winners
from extractors.extract_awards import extract_awards
from extractors.extract_nominees import extract_nominees
from extractors.extract_presenters import extract_presenters
from extractors.extract_hosts import extract_hosts
from extractors.extract_more import extract_more_info

import pickle as pkl


with open("PICKLED_STUFF.pkl", 'rb') as file:
    good_awards_ceremony = pkl.load(file)
    tweets = pkl.load(file)

print("PICKLE LOADED")

extract_more_info(tweets, good_awards_ceremony.get_awards())

