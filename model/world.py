from model.fortress import Fortress
from model.creature import Creature
from model.tilemap import TileMap
from util.point import Point
from util.dice import Dice


class World:
    MAP_SIZE = 10

    def __init__(self, red_player, blue_player):
        self.tilemap = TileMap(World.MAP_SIZE)
        self.creatures = {}
        self.players = {}

        self.red_player = red_player
        self.blue_player = blue_player

        for p in (red_player, blue_player):
            self.players[p] = {'fortress': Fortress(p),
                               'creatures': {}, 
                               'gold': 0}

        self.tilemap.set_tile_at(World.MAP_SIZE - 1, World.MAP_SIZE - 1, self.players[red_player]['fortress'])
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 1, World.MAP_SIZE - 2)))
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 2, World.MAP_SIZE - 1)))

        self.tilemap.set_tile_at(0, 0, self.players[blue_player]['fortress'])
        self.insert_creature(Creature('Peon', blue_player, position=Point(0, 1)))
        self.insert_creature(Creature('Peon', blue_player, position=Point(1, 0)))

    def insert_creature(self, c):
        """
        Inserts a creature into the world.
        """
        self.creatures[c.id] = c
        self.players[c.player]['creatures'][c.id] = c
        self.tilemap.set_tile_at(c.position.x, c.position.y, c)

    def remove_creature(self, c):
        """
        Removes a creature from the world.
        """
        del self.creatures[c.id]
        del self.players[c.player]['creatures'][c.id]
        self.tilemap.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)

    def move_creature(self, c, dx, dy):
        """
        Attempts to move a creature by increasing its x and y.
        """
        to_x = c.position.x + dx
        to_y = c.position.y + dy

        if self.tilemap.in_bounds(to_x, to_y) and self.tilemap.is_tile_empty(to_x, to_y):
            self.tilemap.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)
            self.tilemap.set_tile_at(to_x, to_y, c)
            c.position.x = to_x
            c.position.y = to_y

            return True
        else:
            return False

    def standing_players(self):
        return filter(lambda player: len(self.players[player]['creatures']) > 0, self.players.keys())

    def winner(self):
        # TODO: check stale winning/drawing conditions.
        # (eg: there are no more creatures and Player 1 has not enough resources)
        survivors = self.standing_players()
        if len(survivors) == 1:
            return survivors[0]
        else:
            return None

    def gather_creature_info(self, c):
        """
        Information available to that creature.
        """
        info = {'creatures': {}, 'memory': c.memory}

        x0 = max(c.position.x - c.view_range, 0)
        xf = min(c.position.x + c.view_range, World.MAP_SIZE - 1)
        y0 = max(c.position.y - c.view_range, 0)
        yf = min(c.position.y + c.view_range, World.MAP_SIZE - 1)

        for x in range(x0, xf + 1):
            for y in range(y0, yf + 1):
                if self.tilemap.in_bounds(x, y) and not self.tilemap.is_tile_empty(x, y):
                    creat = self.tilemap.get_tile_at(x, y)
                    creature_info = {
                        'id': creat.id,
                        'name': creat.name,
                        'level': creat.level,
                        'life': creat.life,
                        'player': creat.player,
                        'x': x,
                        'y': y
                    }
                    if creat.id != c.id:
                        info['creatures'][creat.id] = creature_info
                    else:
                        info['myself'] = creature_info

        return info

    def handle_creature_response(self, resp, c):
        """
        Handles a creature's response to the think method.
        """
        c.memory = resp['memory']

        if resp['action'] == 'move':
            dx, dy = resp.get('dx', 0), resp.get('dy', 0)
            self.move_creature(c, dx, dy)
        elif resp['action'] == 'attack':
            target_x, target_y = resp.get('target_x', 0), resp.get('target_y', 0)
            target_creature = self.tilemap.get_tile_at(target_x, target_y)
            if target_creature.__class__ == Creature:
                c.attack(target_creature)
        elif resp['action'] == 'wander':
            self.move_creature(c, Dice.roll(2) - 1, Dice.roll(2) - 1)

    def gather_fortress_info(self, c):
        return

    def handle_fortress_response(self, resp, c):
        return

    def update(self):
        dead_creatures = []

        for id in self.creatures:
            creature = self.creatures[id]

            if not creature.alive():
                dead_creatures.append(creature)
                continue

        self.clean(dead_creatures)

        return self.winner()

    def clean(self, dead_creatures=None):
        for dead in dead_creatures:
            self.remove_creature(dead)