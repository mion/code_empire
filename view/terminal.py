from error import InvalidPlayerError


class Colors:
    """
    ASCII escape codes for terminal colors.
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

    def display(self, current_round):
        """
        Prints the map on the console.
        """
        red = self.world.red_player
        blue = self.world.blue_player

        print 'FORTRESSES'
        print '-'*10
        self.world.players[red]['fortress'].display()
        self.world.players[blue]['fortress'].display()

        print 'CREATURES'
        print '-'*10
        for id in self.world.creatures:
            self.world.creatures[id].display()

        print 'MAP - Round {}'.format(current_round)
        print '-'*10
        print self.str_tilemap()

    def str_tilemap(self):
        tilemap = self.world.tilemap

        s = ''
        header = '  '
        for j in range(tilemap.size):
            header += " {} ".format(j)
        header += "\n"

        for i in range(tilemap.size):
            cols = []
            for j in range(tilemap.size):
                cols.append("[{}]".format(str(tilemap.get_tile_at(j, i))))

            row = ''.join(cols)
            s += "{} {}\n".format(i, row)

        return header+s

    def color_str_creature(self, creature):
        if creature.player == self.world.red_player:
            return Colors.RED + str(creature) + Colors.END
        elif creature.player == self.world.blue_player:
            return Colors.BLUE + str(creature) + Colors.END
        else:
            raise InvalidPlayerError(creature.player)