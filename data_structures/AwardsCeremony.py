class AwardsCeremony:
  def __init__(self, name, awards, start_time, end_time, location):
    self.name = name
    self.awards = awards
    self.start_time = start_time
    self.end_time = end_time
    self.location = location

  def __str__(self):
    return f"The awards ceremony is {self.name}. It started at {self.start_time} and ended at {self.end_time} at {self.location}. The awards were the following: {self.awards}"

  def get_name(self):
    return self.name

  def get_awards(self):
    return self.awards

  def get_start_time(self):
    return self.start_time

  def get_end_time(self):
    return self.end_time

  def get_location(self):
    return self.location
