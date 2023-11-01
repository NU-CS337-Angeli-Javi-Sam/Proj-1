# CS 337 Project 1 -- Tweet Mining & The Golden Globes
## Collaborators:
- Angeli Mittal
- Javier Cuadra
- Samuel Johnson

## Description
This project attempts to identify the host(s), awards, and associated presenters, nominees, and winners of those awards from a set of Tweets provided for an awards ceremony. This project was developed and tested using the 2013 Golden Globes and was designedto be modular with other years and awards ceremonies. Provided that the user puts a file with a list of tweets in the `data` directory and passes filename and year that awards take place as arguments, we attempt to predict the aforementioned fields.

## Public Github Repository
Link to Repository: [NU-CS337-Angeli-Javi-Sam/Proj-1](https://github.com/NU-CS337-Angeli-Javi-Sam/Proj-1)


## Python Version
v3.10.7

## External Packages Used

- Pandas

## Set-Up

1. Navigate to the `Proj-1` directory
2. Run the following in Terminal (we are using Python v3.10.7):
   1. `python3 -m venv ./venv`
   2. `source venv/bin/activate`
   3. `pip3 install -r requirements.txt`


## Running Program

1. Run `python3 gg_api.py {filename} {year}`
   - `{filename}` is the filename containing the tweets for the awards ceremony.
   - `{year}` is the year the awards ceremony took place
   - If left without `{filename}` or `{year}`, it will default to 2013's data.


## Output

The output of this script is two files output to the `output` directory:

1. A text file named `output.txt` containing the following format:

  `Host(s): {hosts}`

  `Award: {award_name}`
  `Presenters: {award_presenters}`
  `Nominees: {award_nominees}`
  `Winner: {award_winner}`

  `TweetStats:`
  `top_mentions: {top_mentions}`
  `top_retweets: {top_retweeted_accs : retweets}`
  `top_hashtags: {top_hashtags}`
  `top_tweeters: {top_tweeters}`


2. A JSON file named `output.json` containing the JSON representation of above:

## Rationale
Our goal for this project was to identify the hosts, awards, and the associated winner, nominees, and presenters of the awards. We immediately found that it would be impossible to find the exact names of the awards and at times near impossible to find the presenters or nominees and which award they belong to. We chose to provide a logical approach to the problem as opposed to a complete approach since that would be near impossible.

We will break down our rationale for how we searched for each of the fields we were required to look for: hosts, awards, winner of award, nominees of award, and presenters of award.

### Awards
For the awards, we had to be flexible with award name restrictions to identify the most reliable award names, often favoring colloquial terms over official ones for the sake of generalization and easier award recognition. Examples include "Best Director - Motion Picture" being simplified to "Best Director" and "Lifetime Achievement Award" being transformed into "Cecil B. DeMille Award." The awards system processes a list of tweets, with each tweet represented as an object containing its original text and other metadata.

To achieve this, we executed two sets of regexes on these tweets. The first set searched for award names that include "Best" and possibly "award" or contain the phrase "Lifetime achievement." After identifying potential award references, the second set of regular expressions confirmed the context: Is the sentence discussing someone winning an award, or is the mention of the word "award" coincidental? Following this verification, we prioritized award titles in title case, aiming for more formal and consistent naming. We also merged similar award names with 67% similarity.

Once we gathered this data, we attempted to eliminate invalid awards by cross-referencing them with a list of valid keywords in the dataset. We also continued to remove awards as we acquired more information about the winners, nominees, and so on. Using keyword validation and logical analysis proved to be the most efficient method for this task. Given more time, we would have explored this approach further.

### Winners
Winners receives our list of award names and tweet objects. We then created regex patterns for each award name to scan the tweets for mentions of award names alongside winner names. Upon finding a potential match, we applied another regex to extract the award winner's name. This process generated a list of potential winners, which we associated with their respective award names.

Subsequently, we merged all winner names based on a similarity ratio of approximately 67%. We initiated our first check for award validity, removing awards that didn't meet our threshold for potential winners, typically around 3, to eliminate invalid awards. This left us with valid awards and potentially valid winner names.

We attempted to incorporate a function that could determine whether the winner should be a human or a movie based on the award name. However, this proved challenging to implement effectively. For example, in categories like "Best Original Song," we often obtained the songwriters' names rather than the movie in which the song featured. Nonetheless, our matching process remained fairly accurate due to subsequent verification practices downstream.

### Nominees
Nominees follows a similar process to our other extraction methods. It is provided with a dictionary of awards to winners and creates a new dictionary of awards linked to a SortedDict of nominees using those keys. Next, it extracts the most likely winner from the awards to winner dictionary and uses that, along with the award name, to guide its search through the list of tweet objects we are working with. We then filter out invalid entries in the nominee list and return our awards to nominee data structure.

This method is relatively straightforward. We had planned to implement a way to distinguish between the names of individuals and those of movies, similar to our approach for winners, but this feature isn't fully realized as intended. Nevertheless, the accuracy remains high, and the method proves effective.

### Hosts
For the hosts, we ran two searches in the dataset. First, we attempted to find all tweets matching the regex for the word host followed by a name, represented as a title-cased bi-gram. From those tweets, we identified all names within the tweets. We then stored those values and enumerated all instances of those names mentioned.

Next, we located all tweets containing a name and the words 'opening monologue', and extracted all instances of names from the tweet. For each name, we checked if the name was already recorded from the previous search, and if so, we incremented the count.

By the end of both searches, we found two potential hosts, in this case Amy Poehler and Tina Fey. We recognize that the number of hosts an awards ceremony has can vary (primarily between one and two), so we propose a future improvement to our search would be to include some threshold that, if met, would categorize a name as a potential host. An example would be measuring the relative difference of all name's occurence count against the maximum occurence count and categorizing the names who have a difference of about 10% from the maximum as a potential host.

### Presenters
For our search of presenters, we searched all tweets for names followed by a variation of a word representing the act of presenting (i.e, introduces, announces, presents, etc.). From those tweets, we then filtered any that were retweets.

Next we filtered the remaining tweets based on those that mentioned the award names we previously determined to be likely awards. We grouped all tweets based on the probable award name and then proceeded to extract the names from the tweets.

The names we found were the most likely presenters for the given award. This was not an exhaustive search; however, it was a the most straightforward approach to searching for presenters. We believe we could improve on this search by using temporal data to segment the tweets based on likelihood of award presentation. From this, we would be able to apply less obvious queries such as finding tweets where jokes are mentioned, filtering the names of probable hosts and winners (since they may joke when hosting or accepting awards, respectively), and counting occurences of names.

## BONUS: TweetStats
Tweetstats was originally created to collect meta data on our tweet dataset to inform our search for data extraction regex patterns. It operates through four internal SortDict objects, which are structured to allow retrieval of keys in ascending order based on their values.

For hashtags, mentions, usernames, and retweeted tweets, Tweetstats tallies their frequencies, storing the data as "name to count" key-value pairs in respective internal SortedDicts. Retweeted accounts are counted, and each retweet is associated with the original account in a regular dictionary,  mapping popular retweeted accounts to their specific retweeted tweets via their usernames.

We initially implemented a histogram feature in the TweetHistogram object to create word clouds by mapping words to their appearance counts over a specified time period, this feature had to be commented out due to its extensive runtime. The TweetHistogram is still there and it contains a list of tweets and a SortDict with unique words as keys and their respective counts as values.
