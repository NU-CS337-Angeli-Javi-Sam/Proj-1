class Entity:
  def __init__(self, name):
    self.__name = name

  def __str__(self):
    return f"{self.get_name()}"

  def get_name(self):
    return self.__name

  def set_name(self, name):
    self.__name = name
