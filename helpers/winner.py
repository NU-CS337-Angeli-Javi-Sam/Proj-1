def get_winners_dict(awards_ceremony):
  winners_dict = dict()

  for award in awards_ceremony.get_awards():
    winners_dict[award.get_name()] = award.get_winner()

  return winners_dict
