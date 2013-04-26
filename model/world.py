from model.fortress import Fortress
from model.creature import Creature
from util.point import Point


class World:
    MAP_SIZE = 10

    def __init__(self, red_player, blue_player):
        self.tile_map = TileMap(World.MAP_SIZE)
        self.creatures = {}
        self.players = {}

        self.red_player = red_player
        self.blue_player = blue_player

        for p in (red_player, blue_player):
            self.players[p] = {'fortress': Fortress(p),
                               'creatures': {}, 
                               'gold': 0}

        self.tile_map.set_tile_at(World.MAP_SIZE - 1, World.MAP_SIZE - 1, self.players[red_player]['fortress'])
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 1, World.MAP_SIZE - 2)))
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 2, World.MAP_SIZE - 1)))

        self.tile_map.set_tile_at(0, 0, self.players[blue_player]['fortress'])
        self.insert_creature(Creature('Peon', blue_player, position=Point(0, 1)))
        self.insert_creature(Creature('Peon', blue_player, position=Point(1, 0)))

    def insert_creature(self, c):
        """
        Inserts a creature into the world.
        """
        self.creatures[c.id] = c
        self.players[c.player]['creatures'][c.id] = c
        self.tile_map.set_tile_at(c.position.x, c.position.y, c)

    def remove_creature(self, c):
        """
        Removes a creature from the world.
        """
        del self.creatures[c.id]
        del self.players[c.player]['creatures'][c.id]
        self.tile_map.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)

    def move_creature(self, c, dx, dy):
        """
        Attempts to move a creature by increasing its x and y.
        """
        to_x = c.position.x + dx
        to_y = c.position.y + dy

        if self.tile_map.in_bounds(to_x, to_y) and self.tile_map.is_tile_empty(to_x, to_y):
            self.tile_map.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)
            self.tile_map.set_tile_at(to_x, to_y, c)
            c.position.x = to_x
            c.position.y = to_y

            return True
        else:
            return False

    def standing_players(self):
        return filter(lambda player: len(self.players[player]['creatures']) > 0, self.players.keys())

    def has_winner(self):
        survivors = self.standing_players()
        if len(survivors) <= 1:
            return False
        else:
            return True


    def gather_creature_info(self, c):
        """
        Information available to that creature.
        """
        info = {'creatures': []}

        x0 = max(c.position.x - c.view_range, 0)
        xf = min(c.position.x + c.view_range, World.MAP_SIZE - 1)
        y0 = max(c.position.y - c.view_range, 0)
        yf = min(c.position.y + c.view_range, World.MAP_SIZE - 1)

        for x in range(x0, xf + 1):
            for y in range(y0, yf + 1):
                if self.tile_map.in_bounds(x, y) and not self.tile_map.is_tile_empty(x, y):
                    c = self.tile_map.get_tile_at(x, y)
                    creature_info = {
                        'id': c.id,
                        'name': c.name,
                        'level': c.level,
                        'life': c.life,
                        'player': c.player,
                        'x': x,
                        'y': y
                    }
                    info['creatures'].append(creature_info)

        return info

    def handle_creature_response(self, resp, c):
        """
        Handles a creature's response to the think method.
        """
        if resp['action'] == 'move':
            dx, dy = resp.get('dx', 0), resp.get('dy', 0)
            self.move_creature(c, dx, dy)
        elif resp['action'] == 'attack':
            target_x, target_y = resp.get('target_x', 0), resp.get('target_y', 0)
            target_creature = self.tile_map.get_tile_at(target_x, target_y)
            if target_creature.__class__ == Creature:
                c.attack(target_creature)

    def gather_fortress_info(self, c):
        return

    def handle_fortress_response(self, resp, c):
        return

    def update(self):
        dead_creatures = []

        for id in self.creatures:
            creature = self.creatures[id]

            if not creature.alive():
                #self.remove_creature(creature)
                dead_creatures.append(creature)
                continue

            info = self.gather_creature_info(creature)
            response = creature.think(info)
            self.handle_creature_response(response, creature)

        self.clean(dead_creatures)

        return self.has_winner()

    def clean(self, dead_creatures=None):
        for dead in dead_creatures:
            self.remove_creature(dead)


class TileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TileMap:
    EMPTY_TILE = ' '

    def __init__(self, size):
        self.size = size
        self.tiles = []
        for i in range(size*size):
            self.tiles.append(self.EMPTY_TILE)

    def get_tile_at(self, x, y):
        if self.in_bounds(x, y):
            return self.tiles[x + self.size*y]
        else:
            raise TileError('point ({}, {}) out of bounds'.format(x, y))

    def set_tile_at(self, x, y, tile):
        if self.in_bounds(x, y):
            self.tiles[x + self.size*y] = tile
        else:
            raise TileError('point ({}, {}) out of bounds'.format(x, y))

    def is_tile_empty(self, x, y):
        if self.in_bounds(x, y):
            return self.get_tile_at(x, y) == self.EMPTY_TILE
        else:
            raise TileError('point ({}, {}) out of bounds'.format(x, y))

    def in_bounds(self, x, y):
        return (0 <= x < self.size) and (0 <= y < self.size)

    def __str__(self):
        s = ''
        header = '  '
        for j in range(self.size):
            header += " {} ".format(j)
        header += "\n"

        for i in range(self.size):
            cols = []
            for j in range(self.size):
                cols.append("[{}]".format(str(self.get_tile_at(j, i))))

            row = ''.join(cols)
            s += "{} {}\n".format(i, row)

        return header+s