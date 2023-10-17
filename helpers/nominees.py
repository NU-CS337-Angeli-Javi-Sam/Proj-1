from utils.create_dict import create_dict
from utils.import_awards_ceremony import import_awards_ceremony

def get_nominees_dict(year):
    """
    Get a dictionary of nominees for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the nominees.

    Returns:
    - nominees_dict (dict): A dictionary containing nominees for different award categories.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Create a dictionary of nominees using the 'create_dict' function.
    nominees_dict = create_dict(awards_ceremony, "Nominees")

    return nominees_dict
