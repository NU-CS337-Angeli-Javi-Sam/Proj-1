import re
from utils.import_awards_ceremony import import_awards_ceremony
from utils.regex import HOST_REGEX, NAME_REGEX, OPENING_MONOLOGUE_REGEX


def get_hosts_list(year):
    """
    Get the list of hosts for a specific awards ceremony year.

    Parameters:
    - year (int): The year of the awards ceremony for which you want to retrieve the hosts.

    Returns:
    - hosts (list): A list of hosts for the specified awards ceremony year.
    """
    awards_ceremony = import_awards_ceremony(year)

    # Retrieve the list of hosts from the awards ceremony data.
    hosts = awards_ceremony.get("Host", [])

    return hosts
