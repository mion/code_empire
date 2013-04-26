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
    ENDC 	= '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

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
        print self.world.tile_map