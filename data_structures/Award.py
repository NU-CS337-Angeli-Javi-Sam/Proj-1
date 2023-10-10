class Award:
  def __init__(self, name, presenters, nominees, winner):
    self.name = name
    self.presenters = presenters
    self.nominees = nominees
    self.winner = winner

  def __str__(self):
    presenters_str = " & ".join(self.presenters)
    first_sentence = f"{self.name} was presented by {presenters_str}."

    if len(self.nominees) == 0:
      second_sentence = "There were no nominees and the winner was {self.winner}."
    else:
      nominees_str = ", ".join(self.nominees)
      second_sentence = f"The nominees were {nominees_str} and the winner was {self.winner}."

    return f"{first_sentence} {second_sentence}"

  def get_name(self):
    return self.name

  def get_presenters(self):
    return self.presenters

  def get_nominees(self):
    return self.nominees

  def get_winner(self):
    return self.winner
