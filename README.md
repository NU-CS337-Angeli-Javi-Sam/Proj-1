# CS 337 Project 1 -- Tweet Mining & The Golden Globes
## Collaborators:
- Angeli Mittal
- Javier Cuadra
- Samuel Johnson

## Description
This project attempts to identify the host(s), awards, and associated presenters, nominees, and winners of those awards from a set of Tweets provided for an awards ceremony. This project was developed and tested using the 2013 Golden Globes and was designedto be modular with other years and awards ceremonies. Provided that the user puts a file with a list of tweets in the `data` directory and passes filename and year that awards take place as arguments, we attempt to predict the aforementioned fields.

## Public Github Repository
Link to Repository: [NU-CS337-Angeli-Javi-Sam/Proj-1](https://github.com/NU-CS337-Angeli-Javi-Sam/Proj-1)


## External Packages Used

-
-
-

## Set-Up

1. Navigate to the `Proj-1` directory
2. Run the following in Terminal:
   1. `python3 -m venv ./venv`
   2. `source venv/bin/activate`
   3. `pip3 install -r requirements.txt`


## Running Program

1. Run `python3 gg_api.py {filename} {year}`
   - `{filename}` is the filename containing the tweets for the awards ceremony.
   - `{year}` is the year the awards ceremony took place


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

### Hosts
For the hosts, we ran two searches in the dataset. First, we attempted to find all tweets matching the regex for the word host followed by a name, represented as a title-cased bi-gram. From those tweets, we identified all names within the tweets. We then stored those values and enumerated all instances of those names mentioned.

Next, we located all tweets containing a name and the words 'opening monologue', and extracted all instances of names from the tweet. For each name, we checked if the name was already recorded from the previous search, and if so, we incremented the count.

By the end of both searches, we found two potential hosts, in this case Amy Poehler and Tina Fey. We recognize that the number of hosts an awards ceremony has can vary (primarily between one and two), so we propose a future improvement to our search would be to include some threshold that, if met, would categorize a name as a potential host. An example would be measuring the relative difference of all name's occurence count against the maximum occurence count and categorizing the names who have a difference of about 10% from the maximum as a potential host.

### Presenters

For our search of presenters, we searched all tweets for names followed by a variation of a word representing the act of presenting (i.e, introduces, announces, presents, etc.). From those tweets, we then filtered any that were retweets.

Next we filtered the remaining tweets based on those that mentioned the award names we previously determined to be likely awards. We grouped all tweets based on the probable award name and then proceeded to extract the names from the tweets.

The names we found were the most likely presenters for the given award. This was not an exhaustive search; however, it was a the most straightforward approach to searching for presenters. We believe we could improve on this search by using temporal data to segment the tweets based on likelihood of award presentation. From this, we would be able to apply less obvious queries such as finding tweets where jokes are mentioned, filtering the names of probable hosts and winners (since they may joke when hosting or accepting awards, respectively), and counting occurences of names.

## BONUS: TweetStats
