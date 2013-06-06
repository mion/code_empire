from random import randrange
from util.point import Point


class Entity(object):
    """Entity"""
    ID_COUNTER = randrange(0, 101) # Add random initial ID to avoid cheating (finding the other player's creatures).

    def __init__(self, position):
        self.id = str(Entity.ID_COUNTER)
        Entity.ID_COUNTER += randrange(1, 101)
        self.position = position


class EntityADT(object):
    """Entity Abstract Data Type"""
    def __init__(self):
        self.entities = {}

    def __len__(self):
        return len(self.entities)

    def insert(self, entity):
        self.entities[entity.id] = entity

    def find_by_id(self, id):
        return self.entities.get(id, None)

    def find_by_pos(self, pos):
        # TODO: improve performance
        for entity in self.entities.itervalues():
            if entity.pos == pos:
                return entity
        return None
