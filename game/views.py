# -*- coding: utf-8 -*-

"""
game.views
~~~~~~~~~~~~~~~~~~~

This module contains graphic logic.
At the moment this means drawing stuff to the terminal.

"""

from models import Creature


class Colors:
    """
    
    """
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    CYAN    = '\033[96m'
    END     = '\033[0m'

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
            red='\033[91m',
            blue='\033[94m',
            green='\033[92m',
            yellow='\033[93m',
            magenta='\033[95m',
            cyan='\033[96m',
            end='\033[0m') # ASCII escape codes for terminal colors.

        self.player_colors = {}
        available_colors = ['magenta', 'cyan', 'green', 'yellow', 'blue', 'red']
        for i, player in enumerate(world.players.iterkeys()):
            self.player_colors[player] = self.colors[available_colors.pop()]

    def display(self, current_round):
        """
        Prints the map on the console.
        """
        print 'FORTRESSES'
        print '-'*10
        for fortress in self.world.fortresses.itervalues():
            print self.player_colors[fortress.player] + repr(fortress) + self.colors['end']

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
        header = '  '.join([str(j) for j in range(tilemap.size)])

        for i in range(tilemap.size):
            row = ''.join([self.str_tile(tilemap.get_tile_at(j, i)) for j in range(tilemap.size)])
            s += "{} {}\n".format(i, row)

        return "   {}\n{}".format(header, s)

    def str_tile(self, tile):
        s = str(tile) if tile else ' '

        if getattr(tile, 'player', None):
            s = self.coloured(s, self.player_colors[tile.player])
        
        return "[{}]".format(s)

    def coloured(self, s, color):
        return color + s + self.colors['end']
