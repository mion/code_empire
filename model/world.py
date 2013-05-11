from model.fortress import Fortress
from model.creature import Creature
from model.resource import Resource
from model.tilemap import TileMap
from util.point import Point
from util.dice import Dice
from util.log import log


class World:
    MAP_SIZE = 10

    def __init__(self, red_player, blue_player):
        self.tilemap = TileMap(World.MAP_SIZE)
        self.creatures = {}
        self.players = {}
        self.resources = {}

        self.red_player = red_player
        self.blue_player = blue_player

        for p in (red_player, blue_player):
            self.players[p] = {'fortress': Fortress(p),
                               'creatures': {}, 
                               'gold': 0}

        self.players[red_player]['fortress'].position = Point(World.MAP_SIZE - 1, World.MAP_SIZE - 1)
        self.insert_fortress(self.players[red_player]['fortress'])
        # self.tilemap.set_tile_at(self.players[red_player]['fortress'].position.x, 
        #                          self.players[red_player]['fortress'].position.y, 
        #                          self.players[red_player]['fortress'])
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 1, World.MAP_SIZE - 2)))
        self.insert_creature(Creature('Peon', red_player, position=Point(World.MAP_SIZE - 2, World.MAP_SIZE - 1)))

        self.players[blue_player]['fortress'].position = Point(0, 0)
        self.insert_fortress(self.players[blue_player]['fortress'])
        # self.tilemap.set_tile_at(self.players[blue_player]['fortress'].position.x, 
        #                          self.players[blue_player]['fortress'].position.y, 
        #                          self.players[blue_player]['fortress'])

        self.insert_creature(Creature('Peon', blue_player, position=Point(0, 1)))
        self.insert_creature(Creature('Peon', blue_player, position=Point(1, 0)))

    def generate_map(self, 
                     init_creatures=2, 
                     init_gold=100, 
                     init_resources=5):
        """
        Randomically place fortresses, starting creatures and resources.

        Keyword arguments:
        init_creatures  -- The number of starting creatures for each player.
        init_gold       -- The amount of starting gold for each player.
        init_resources  -- The number of starting resources scattered around
                           the map. This does NOT include the two large resources
                           that are created near each player's fortress.
        """
        return

    def insert_fortress(self, fortress):
        """
        Insert a fortress into the world.
        """
        self.tilemap.set_tile_at(fortress.position.x, fortress.position.y, fortress)

    def insert_creature(self, c):
        """
        Insert a creature into the world.
        """
        self.creatures[c.id] = c
        self.players[c.player]['creatures'][c.id] = c
        self.tilemap.set_tile_at(c.position.x, c.position.y, c)

    def remove_creature(self, c):
        """
        Remove a creature from the world.
        """
        del self.creatures[c.id]
        del self.players[c.player]['creatures'][c.id]
        self.tilemap.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)

    def move_creature(self, c, dx, dy):
        """
        Attempt to move a creature by increasing its x and y.
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

    def get_entity_at(self, x, y):
        return self.tilemap.get_tile_at(x, y)

    def standing_players(self):
        return filter(lambda player: len(self.players[player]['creatures']) > 0, self.players.keys())

    def winner(self):
        # TODO: check win/draw special cases.
        # (eg: there are no more creatures and Player 1 has not enough resources)
        survivors = self.standing_players()
        if len(survivors) == 1:
            return survivors[0]
        else:
            return None

    def gather_creature_info(self, c): # TODO: change method name... possible confusion with 'gather' from resource?
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
        Handle a creature's response to the think method.
        """
        c.memory = resp['memory']

        # TODO: check for errors (e.g.: 'target' is there but no 'target_x', target class, etc)
        # TODO: optional 'target_id' or 'target_x' and 'target_y'

        if resp['action'] == 'move':
            dx, dy = resp.get('dx', 0), resp.get('dy', 0)
            self.move_creature(c, dx, dy)

        elif resp['action'] == 'attack':
            target_x, target_y = resp.get('target_x', 0), resp.get('target_y', 0)
            target_creature = self.tilemap.get_tile_at(target_x, target_y)
            if target_creature.__class__ == Creature:
                c.attack(target_creature)

        elif resp['action'] == 'gather':
            resource_x, resource_y = resp.get('resource_x', 0), resp.get('resource_y', 0)
            target_resource = self.tilemap.get_tile_at(resource_x, resource_y)
            if target_resource.__class__ == Resource:
                c.gather(target_resource)

        elif resp['action'] == 'wander':
            self.move_creature(c, Dice.roll(2) - 1, Dice.roll(2) - 1)

        if resp.get('log', None):
            for l in resp['log']:
                log(l, "{}'s {} at {}".format(c.player, c.name, c.position))

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