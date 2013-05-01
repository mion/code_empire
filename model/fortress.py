from model.creature import Creature

class Fortress(Creature):
  def __init__(self, player, position=None):
    Creature.__init__(self, 'Fortress', player, 10, position)

  def __str__(self):
    return 'F'

  def think(self, info):
    return