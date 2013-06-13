# -*- coding: utf-8 -*-

"""
game.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power CodeEmpire.

"""

from exceptions import OutOfBoundsError


class EntityCollection(object):
    """Entity collection."""
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


class TileMap(object):
    EMPTY_TILE = ' '

    def __init__(self, size):
        self.size = size
        self.tiles = []
        for i in range(size*size):
            self.tiles.append(self.EMPTY_TILE)

    def in_bounds(self, x, y):
        return (0 <= x < self.size) and (0 <= y < self.size)

    def check_bounds(func):
        def wrapper(self, x, y, *args, **kwargs):
            if self.in_bounds(x, y):
                return func(self, x, y, *args, **kwargs)
            else:
                raise OutOfBoundsError(x, y)
        return wrapper

    @check_bounds
    def get_tile_at(self, x, y):
        return self.tiles[x + self.size*y]

    @check_bounds
    def set_tile_at(self, x, y, tile):
        self.tiles[x + self.size*y] = tile

    @check_bounds
    def is_tile_empty(self, x, y):
        return self.get_tile_at(x, y) == self.EMPTY_TILE

