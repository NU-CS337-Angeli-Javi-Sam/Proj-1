def get_awards_list(awards_ceremony):
  return [award.get_name() for award in awards_ceremony.get_awards()]
