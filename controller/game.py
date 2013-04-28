import os
from model.creature import Creature
from model.fortress import Fortress
from model.world import World
from view.terminal import Terminal


class Game(object):
    MAX_ROUNDS = 500

    def __init__(self, red_player, blue_player):
        self.world = World(red_player, blue_player)
        self.terminal = Terminal(self.world)

    def start(self, interactive=True):
        for i in range(Game.MAX_ROUNDS):
            if interactive:
                self.terminal.display(i + 1)

            #info = self.world.gather_info

            winner = self.world.update()

            if winner:
                if interactive:
                    print 'GAME OVER: {} won!\n'.format(winner)
                break

            if interactive:
                raw_input('Press any key to continue...')

        if interactive:
            print 'GAME OVER: draw.\n'