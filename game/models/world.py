import random
from sets import Set

from model.fortress import Fortress
from model.fortress import FortressADT
from model.creature import Creature
from model.creature import CreatureADT
from model.resource import Resource
from model.resource import ResourceADT
from model.tilemap import TileMap
from util.point import Point
from util.dice import Dice
from util.log import log


class Error(Exception):
    """Base class for errors in this module."""
    pass


class UnknownActionError(Error):
    """Raised when no method handles the action from the AI message."""
    def __init__(self, action):
        self.action = action


class World:
    MAP_SIZE = 9 # Always an odd number!
    STARTING_AREA_SIZE = 3

    def __init__(self, *player_names):
        self.tilemap = TileMap(World.MAP_SIZE)
        self.creatures = {} #CreatureADT()
        self.resources = {} #ResourceADT()
        self.fortresses = {} #FortressADT()
        self.players = {} # maps player_name (string) to a dict
        for player_name in player_names:
            self.players[player_name] = dict(fortress=None, creatures=Set([]))

    def get_entity_at(self, x, y):
        return self.tilemap.get_tile_at(x, y)

    def generate(self, random):
        # For now, hard code 2 players
        self.generate_starting_area(
            random, 
            self.players.keys()[0], 
            Point(World.MAP_SIZE - World.STARTING_AREA_SIZE), 
            Point(World.MAP_SIZE))

        self.generate_starting_area(
            random, 
            self.players.keys()[1], 
            Point(0), 
            Point(World.STARTING_AREA_SIZE))

    def generate_starting_area(self,
                               random,
                               player,
                               lower,
                               upper,
                               num_creatures=2,
                               start_gold=100,
                               num_resources=1,
                               gold_amount_func=lambda i: 100 / (i + 1),
                               gold_flux_func=lambda i: 10 * (i + 1)):
        """
        Randomically place fortresses, starting creatures and resources.

        Keyword arguments:
        random         -- Python's random module.
        player         -- The player's name.
        lower          -- 
        upper          -- 
        num_creatures  -- The number of starting creatures for each player.
        start_gold     -- The amount of starting gold for each player.
        num_resources  -- The number of starting resources scattered around
                           the map, one of which is a large resource
                           that is created near each player's fortress.
        """
        random_points = Point.generate(random,
                                       lower=lower,
                                       upper=upper,
                                       count=(1 + num_creatures + num_resources))

        self.insert_fortress(Fortress(player, start_gold, position=random_points.pop()))

        for i in range(num_creatures):
            self.insert_creature(Creature('Peon', player, position=random_points.pop()))

        for i in range(num_resources):
            self.insert_resource(Resource('Gold Mine', gold_amount_func(i), gold_flux_func(i), position=random_points.pop()))

    def insert_fortress(self, f):
        self.fortresses[f.id] = f
        self.players[f.player]['fortress'] = f
        self.tilemap.set_tile_at(f.position.x, f.position.y, f)

    def insert_creature(self, c):
        self.creatures[c.id] = c
        self.players[c.player]['creatures'].add(c)
        self.tilemap.set_tile_at(c.position.x, c.position.y, c)

    def insert_resource(self, r):
        self.resources[r.id] = r
        self.tilemap.set_tile_at(r.position.x, r.position.y, r)

    def remove_creature(self, c):
        del self.creatures[c.id]
        self.players[c.player]['creatures'].remove(c)
        self.tilemap.set_tile_at(c.position.x, c.position.y, TileMap.EMPTY_TILE)

    def move_creature(self, c, dx, dy):
        """
        Attempt to move a creature by a incrementing its x and y.
        Returns True if successful, False otherwise.
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
        return [p for p in self.players.values() if len(p['creatures']) > 0]

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
        info = {'creatures': {}, 'fortresses': {}, 'resources': {}, 'memory': c.memory}

        x0 = max(c.position.x - c.view_range, 0)
        xf = min(c.position.x + c.view_range, World.MAP_SIZE - 1)
        y0 = max(c.position.y - c.view_range, 0)
        yf = min(c.position.y + c.view_range, World.MAP_SIZE - 1)

        for x in range(x0, xf + 1):
            for y in range(y0, yf + 1):
                if self.tilemap.in_bounds(x, y) and not self.tilemap.is_tile_empty(x, y):
                    entity = self.tilemap.get_tile_at(x, y)
                    if entity.id != c.id:
                        entity_info = entity.to_info()
                        info[entity_info['type']][entity.id] = entity_info # REFACTOR: confusing?
                    else:
                        info['myself'] = entity.to_info()

        return info

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

    def handle_move(self, c, resp):
            dx, dy = resp.get('dx', 0), resp.get('dy', 0)
            self.move_creature(c, dx, dy)

    def handle_attack(self, c, resp):
        target_x, target_y = resp.get('target_x', 0), resp.get('target_y', 0)
        target_creature = self.tilemap.get_tile_at(target_x, target_y)
        if target_creature.__class__ == Creature:
            c.attack(target_creature)

    def handle_gather(self, c, resp):
        resource_x, resource_y = resp.get('resource_x', 0), resp.get('resource_y', 0)
        target_resource = self.tilemap.get_tile_at(resource_x, resource_y)
        if target_resource.__class__ == Resource:
            c.gather(target_resource)

    def handle_wander(self, c, resp):
        self.move_creature(c, Dice.roll(2) - 1, Dice.roll(2) - 1)

    def handle_creature_response(self, resp, c):
        """
        Handle a creature's response to the think method.
        """
        c.memory = resp['memory']

        # All possible actions a creature may perform.
        # TODO: Set this table as a Class constant, as this is probably slow.
        handle = {
            'move':     self.handle_move,
            'attack':   self.handle_attack,
            'gather':   self.handle_gather,
            'wander':   self.handle_wander
        }.get(resp['action'], None)

        if handle:
            handle(c, resp) # Calls the handler method
        else:
            raise UnknownActionError(action=resp['action'])

        # TODO: Check for errors (e.g.: 'target' is there but no 'target_x', target class, etc)
        # TODO: Add optional choice of 'target_id' over 'target_x' and 'target_y'
        if resp.get('log', None):
            for l in resp['log']:
                log(l, "{}'s {} at {}".format(c.player, c.name, c.position))
