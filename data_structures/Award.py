class Award:
  def __init__(self, name, presenters, nominees, winner):
    self.__name = name
    self.__presenters = presenters
    self.__nominees = nominees
    self.__winner = winner

  def __str__(self):
    output = f"Award: {self.get_name().title()}\n"
    output += f"Presenters: {', '.join(self.get_presenters()).title()}\n"
    output += f"Nominees: {', '.join(self.get_nominees()).title()}\n"
    output += f"Winner: {self.get_winner().title()}\n"

    return output

  def get_name(self):
    return self.__name

  def get_presenters(self):
    return self.__presenters

  def get_nominees(self):
    return self.__nominees

  def get_winner(self):
    return self.__winner

  def to_json(self):
    award_dict = {
        "Presenters": [presenter.title() for presenter in self.get_presenters()],
        "Nominees": [nominee.title() for nominee in self.get_nominees()],
        "Winner": self.get_winner().title()
    }
    return award_dict
