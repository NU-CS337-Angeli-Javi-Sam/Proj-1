class AwardsCeremony:
  def __init__(self, name,location, start_time, end_time, hosts, awards):
    self.name = name
    self.location = location
    self.start_time = start_time
    self.end_time = end_time
    self.hosts = hosts
    self.awards = awards

  def __str__(self):
    output = f"Host: {self.hosts}\n"
    for award in self.awards:
      output += f"Award: {award.name}\n"
      output += f"Presenters: {', '.join(award.presenters)}\n"
      output += f"Nominees: \"{', '.join(award.nominees)}\"\n"
      output += f"Winner: \"{award.winner}\"\n"
    return output

  def get_name(self):
    return self.name

  def get_location(self):
    return self.location

  def get_start_time(self):
    return self.start_time

  def get_end_time(self):
    return self.end_time

  def get_hosts(self):
    return self.hosts

  def get_awards(self):
    return self.awards

  def to_json(self):
    ceremony_dict = {
        "Host": self.hosts,
    }

    for award in self.awards:
        ceremony_dict[award.name] = award.to_json()

    return ceremony_dict
