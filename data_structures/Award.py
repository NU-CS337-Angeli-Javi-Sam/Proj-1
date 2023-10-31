class Award:
    """
    Represents an award category with information about the award name, presenters, nominees, and the winner.
    """

    def __init__(self, name, presenters, nominees, winner):
        """
        Initializes an Award object with provided details.

        Parameters:
        - name (str): The name of the award category.
        - presenters (list of str): List of presenters for the award.
        - nominees (list of str): List of nominees for the award.
        - winner (str): The name of the award winner.

        Returns:
        - Award: An Award object.
        """
        self.__name = name
        self.__presenters = presenters
        self.__nominees = nominees
        self.__winner = winner

    def __str__(self):
        """
        Returns a string representation of the Award object.

        Returns:
        - str: A formatted string containing award details.
        """
        output = f"Award: {self.get_name().title()}\n"
        output += f"Presenters: {', '.join(self.get_presenters()).title()}\n"
        output += f"Nominees: {', '.join(self.get_nominees()).title()}\n"
        output += f"Winner: {self.get_winner().title()}\n"

        return output

    def get_name(self):
        """
        Get the name of the award.

        Returns:
        - str: The name of the award.
        """
        return self.__name

    def get_presenters(self):
        """
        Get the list of presenters for the award.

        Returns:
        - list of str: List of presenters' names.
        """
        return self.__presenters

    def get_nominees(self):
        """
        Get the list of nominees for the award.

        Returns:
        - list of str: List of nominees' names.
        """
        return self.__nominees

    def get_winner(self):
        """
        Get the name of the award winner.

        Returns:
        - str: The name of the award winner.
        """
        return self.__winner

    def to_json(self):
        """
        Convert the Award object to a JSON-compatible dictionary.

        Returns:
        - dict: A dictionary containing award details.
        """
        award_dict = {
            "Presenters": [presenter.title() for presenter in self.get_presenters()],
            "Nominees": [nominee.title() for nominee in self.get_nominees()],
            "Winner": self.get_winner().title(),
        }
        return award_dict
