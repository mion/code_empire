class TileMap:
    EMPTY_TILE = ' '

    def __init__(self, size):
        self.size = size
        self.tiles = []
        for i in range(size*size):
            self.tiles.append(self.EMPTY_TILE)

    def get_tile_at(self, x, y):
        return self.tiles[x + self.size*y]

    def set_tile_at(self, tile, x, y):
        self.tiles[x + self.size*y] = tile

    def is_tile_empty(self, x, y):
        return self.get_tile_at(x, y) == self.EMPTY_TILE

    def __str__(self):
        s = ''
        header = '  '
        for j in range(self.size):
            header += " {} ".format(j)
        header += "\n"

        for i in range(self.size):
            row = ''
            for j in range(self.size):
                row += "[{}]".format(str(self.get_tile_at(j, i)))

            s += "{} {}\n".format(i, row)

        return header+s