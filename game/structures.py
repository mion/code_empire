# -*- coding: utf-8 -*-

"""
game.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power CodeEmpire.

"""

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
