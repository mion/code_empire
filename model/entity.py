import random


class Entity(object):
    """docstring for Entity"""
    ID_COUNTER = random.randrange(0, 101) # Add random initial ID to avoid cheating (finding the other player's creatures).

    def __init__(self, position):
        self.id = str(Entity.ID_COUNTER)
        Entity.ID_COUNTER += random.randrange(1, 101)
        self.position = position
