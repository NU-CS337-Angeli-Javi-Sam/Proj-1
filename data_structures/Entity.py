class Entity:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return f"{self.name}"

  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name
