# CS 337 Project 1 -- Tweet Mining & The Golden Globes
## Collaborators:
- Angeli Mittal
- Javier Cuadra
- Samuel Johnson

## Description
This project identifies the host(s), awards, and associated presenters, nominees, and winners of those awards from a set of Tweets provided for an awards ceremony. This project was tested using the 2013 Golden Globes and was designed and developed to be modular. Provided that the user puts a file with a list of tweets in the `data` directory and passes filename and year that awards take place, we can predict the aforementioned fields.

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

2. A JSON file named `output.json` containing the JSON representation of above:
