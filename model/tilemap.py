from error import OutOfBoundsError


class TileMap:
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