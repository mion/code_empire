# -*- coding: utf-8 -*-

"""
game.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Code Empire.

"""

from exceptions import OutOfBoundsError


class EntityDict(object):
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

    def __init__(self, size, empty=' '):
        self.size = size
        self.tiles = [empty for i in range(size*size)]

    def __getitem__(self, p):
        if isinstance(p, slice):
            region = []
            for x in range(p.start[0], p.stop[0]): # Improve? O(n^2)
                for y in range(p.start[1], p.stop[1]):
                    region.append(self.tiles[x + self.size*y])
            return region
        else:
            return self.get_tile_at(p[0], p[1])

    def __setitem__(self, p, tile):
        self.set_tile_at(p[0], p[1], tile)

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

    def get_region(self, lower, upper):
        """
        Returns a square region delimited by the points (tuples) lower_left and
        upper_right.
        """
        return self.tiles[lower:upper]
