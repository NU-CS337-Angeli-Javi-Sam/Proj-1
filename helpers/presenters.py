from .create_dict import create_dict
from .import_awards_ceremony import import_awards_ceremony

def get_presenters_dict(year):
    """
    Get a dictionary of presenters for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the presenters.

    Returns:
    - presenters_dict (dict): A dictionary containing presenters for different award categories.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Create a dictionary of presenters using the 'create_dict' function.
    presenters_dict = create_dict(awards_ceremony, "Presenters")

    return presenters_dict
