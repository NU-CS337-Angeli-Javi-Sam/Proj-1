import json
import os


def import_awards_ceremony(year):
    """
    Import and return awards ceremony data from a JSON file for a specific year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to import data.

    Returns:
    - awards_ceremony (dict): A dictionary containing awards ceremony data, including award categories,
      nominees, winners, and other details.
    """
    filepath = f"output/output{year}.json"

    # Check if the JSON file exists
    if os.path.exists(filepath):
        # Open and parse the JSON file
        with open(filepath, "r", encoding="utf-8") as json_file:
            try:
                awards_ceremony = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")
    else:
        awards_ceremony = {}  # Initialize an empty dictionary if the file doesn't exist

    return awards_ceremony
