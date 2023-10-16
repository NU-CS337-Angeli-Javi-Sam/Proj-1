class AwardsCeremony:
  def __init__(self, name, location, start_time, end_time, hosts, awards):
    self.__name = name
    self.__location = location
    self.__start_time = start_time
    self.__end_time = end_time
    self.__hosts = hosts
    self.__awards = awards

  def __str__(self):
    output = f"Host: {', '.join(self.get_hosts()).title()}\n\n"
    for award in self.get_awards():
      output += f"{award}\n"
    return output

  def get_name(self):
    return self.__name

  def get_location(self):
    return self.__location

  def get_start_time(self):
    return self.__start_time

  def get_end_time(self):
    return self.__end_time

  def get_hosts(self):
    return self.__hosts

  def get_awards(self):
    return self.__awards

  def to_json(self):
    ceremony_dict = {
        "Host": [host.title() for host in self.get_hosts()],
    }

    for award in self.get_awards():
        ceremony_dict[award.get_name().title()] = award.to_json()

    return ceremony_dict
