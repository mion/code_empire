import random
from model.entity import Entity


class Resource(Entity):
    """
    Creatures get gold from Resources deposits that are scattered across the map.
    """
    def __init__(self, name, gold_amount, gold_flux, position=None):
        """
        :param: name The resource's name (eg: Tree, Gold Mine, etc)
        :param: gold_amount The amount of gold stored in this resource.
        :param: gold_flux The amount of gold that can be retrieved per turn by any creature.
        """
        super(Resource, self).__init__(position=position)

        self.name        = name
        self.gold_amount = gold_amount
        self.gold_flux   = gold_flux

    def __str__(self):
        return '$'

    def __repr__(self):
        return '{} {}, gold: {} [+{}]\n'.format(self.position, self.name, self.gold_amount, self.gold_flux)

    def to_info(self):
        return {
                'id': self.id,
                'name': self.name,
                'type': 'resources',
                'gold_amount': self.gold_amount,
                'gold_flux': self.gold_flux,
                'x': self.position.x,
                'y': self.position.y
               }

    def depleted(self):
        return self.gold_amount <= 0

    def gather(self, gold_flux_cap=None):
        if self.depleted():
            return 0

        if gold_flux_cap:
            gold_extracted = min(gold_flux_cap, self.gold_flux)
        else:
            gold_extracted = self.gold_flux
        
        if self.gold_amount - gold_extracted > 0:
            self.gold_amount -= gold_extracted
            return self.gold_flux
        else:
            remaining_gold = self.gold_amount
            self.gold_amount = 0
            return remaining_gold