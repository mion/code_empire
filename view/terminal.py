from error import InvalidPlayerError
from model.creature import Creature


class Colors:
    """
    
    """
    MAGENTA = '\033[95m'
    BLUE 	= '\033[94m'
    GREEN 	= '\033[92m'
    YELLOW 	= '\033[93m'
    RED 	= '\033[91m'
    CYAN 	= '\033[96m'
    END 	= '\033[0m'

    def disable(self):
        MAGENTA = ''
        BLUE    = ''
        GREEN   = ''
        YELLOW  = ''
        RED     = ''
        CYAN    = ''
        END    = ''


class Terminal:
    def __init__(self, world):
        self.world = world
        self.colors = dict(
            magenta='\033[95m',
            blue='\033[94m',
            green='\033[92m',
            yellow='\033[93m',
            red='\033[91m',
            cyan='\033[96m',
            end='\033[0m') # ASCII escape codes for terminal colors.

        self.player_colors = {}
        for i, player in enumerate(world.players.iterkeys()):
            self.player_colors[player] = self.colors.values()[i]

    def display(self, current_round):
        """
        Prints the map on the console.
        """
        print 'FORTRESSES'
        print '-'*10
        for name, player in self.world.players.iteritems():
            print self.player_colors[name] + repr(player['fortress']) + self.colors['end']

        print 'CREATURES'
        print '-'*10
        for creature in self.world.creatures.itervalues():
            print self.player_colors[creature.player] + repr(creature) + self.colors['end']

        print 'RESOURCES'
        print '-'*10
        for resource in self.world.resources.itervalues():
            print repr(resource)

        print 'MAP - Round {}'.format(current_round)
        print '-'*10
        print self.str_tilemap()

    def str_tilemap(self):
        tilemap = self.world.tilemap

        s = ''
        header = ' '.join([j for j in range(tilemap.size)])

        for i in range(tilemap.size):
            cols = []
            for j in range(tilemap.size):
                tile = tilemap.get_tile_at(j, i)
                if not tilemap.is_tile_empty(j, i):
                    cols.append("[{}]".format(self.str_color(tilemap.get_tile_at(j, i))))
                else:
                    cols.append("[ ]")

            row = ''.join(cols)
            s += "{} {}\n".format(i, row)

        return header+s

    def str_color(self, entity):
        if getattr(entity, 'player', None):
            if entity.player == self.world.red_player:
                return Colors.RED + str(entity) + Colors.END
            elif entity.player == self.world.blue_player:
                return Colors.BLUE + str(entity) + Colors.END
            else:
                raise InvalidPlayerError(entity.player)
        else:
            return str(entity)

    def color_str(self, string, color):
        return color + string + Colors.END