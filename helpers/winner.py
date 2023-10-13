from .create_dict import create_dict
from .import_awards_ceremony import import_awards_ceremony

def get_winners_dict(year):
    """
    Get a dictionary of winners for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the winners.

    Returns:
    - winners_dict (dict): A dictionary containing winners for different award categories.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Create a dictionary of winners using the 'create_dict' function.
    winners_dict = create_dict(awards_ceremony, "Winner")

    return winners_dict
