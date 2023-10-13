from .import_awards_ceremony import import_awards_ceremony

def get_awards_list(year):
    """
    Get a list of award categories for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the award categories.

    Returns:
    - award_categories (list): A list of award categories for the specified awards ceremony year.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Retrieve a list of award categories by excluding the first key in the dictionary (usually the awards ceremony name).
    award_categories = list(awards_ceremony.keys())[1:]

    return award_categories
