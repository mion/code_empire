import world

if __name__ == '__main__':
    tile_map = world.TileMap(10)
    tile_map.set_tile_at('x', 3, 5)
    print tile_map