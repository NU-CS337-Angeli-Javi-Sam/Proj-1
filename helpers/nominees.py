def get_nominees_dict(awards_ceremony):
  nominees_dict = dict()

  for award in awards_ceremony.get_awards():
    nominees_dict[award.get_name()] = award.get_nominees()

  return nominees_dict
