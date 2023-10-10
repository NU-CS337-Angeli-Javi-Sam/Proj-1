def get_presenters_dict(awards_ceremony):
  presenters_dict = dict()

  for award in awards_ceremony.get_awards():
    presenters_dict[award.get_name()] = award.get_presenters()

  return presenters_dict
