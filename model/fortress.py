from model.creature import Creature
from model.creature import CreatureADT

class Fortress(Creature):
    def __init__(self, player, gold_carried=100, position=None):
        super(Fortress, self).__init__('Fortress', player, 10, position)
        self.gold_carried = gold_carried

    def __str__(self):
        return 'F'

    def to_info(self):
        return {
                'id': self.id,
                'name': self.name,
                'type': 'fortresses',
                'level': self.level,
                'life': self.life,
                'player': self.player,
                'x': self.position.x,
                'y': self.position.y
               }

    def think(self, info):
        return


class FortressADT(CreatureADT):
    """Fortress Abstract Data Type"""
    def __init__(self):
        super(FortressADT, self).__init__()
