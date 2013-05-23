from model.creature import Creature

class Fortress(Creature):
    def __init__(self, player, position=None):
        super(Fortress, self).__init__('Fortress', player, 10, position)

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