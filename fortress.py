from creature import Creature

class Fortress(Creature):
  def __init__(self, player):
    Creature.__init__(self, 'Fortress', player, 10)

  def __str__(self):
    return 'F'

  def think(self, info):
    return