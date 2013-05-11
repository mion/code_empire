import random

class Resource(object):
    """
    Creatures get gold from Resources deposits that are scattered across the map.
    """

    ID_COUNTER = random.randrange(0, 101) # Add random initial ID to avoid cheating (finding the other player's creatures).

    def __init__(self, name, gold_amount, gold_flux, position=None):
        """
        :param: name The resource's name (eg: Tree, Gold Mine, etc)
        :param: gold_amount The amount of gold stored in this resource.
        :param: gold_flux The amount of gold that can be retrieved per turn by any creature.
        """
        self.id = str(Resource.ID_COUNTER)
        Resource.ID_COUNTER += random.randrange(1, 101)

        self.name        = name
        self.gold_amount = gold_amount
        self.gold_flux   = gold_flux
        self.position    = position

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