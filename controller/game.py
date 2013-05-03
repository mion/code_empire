import sys
import subprocess
import json
import md5
from random import random
from model.creature import Creature
from model.fortress import Fortress
from model.world import World
from view.terminal import Terminal


class Game(object):
    MAX_ROUNDS = 500

    def __init__(self, red_player, blue_player):
        self.world = World(red_player, blue_player)
        self.terminal = Terminal(self.world)

    def random_hash(self):
        return md5.new(str(random())).hexdigest()

    def start(self, interactive=True):
        if interactive:
                self.terminal.display(0)

        for i in range(Game.MAX_ROUNDS):
            creatures = self.world.creatures

            for id in creatures:
                info = self.world.gather_creature_info(creatures[id])
                info_json = json.dumps(info)
                try:
                    # TODO: review security issue with check_output (possibly malicious player name?)
                    response_json = subprocess.check_output(["./ai/{}/think.sh '{}'".format(creatures[id].player, info_json)], shell=True)
                    response = json.loads(response_json)
                    self.world.handle_creature_response(response, creatures[id])
                except subprocess.CalledProcessError, e:
                    print '\nAn error occurred when running think.sh: ' + str(e)
                    sys.exit(1)

            if interactive:
                self.terminal.display(i + 1)

            winner = self.world.update()

            if winner:
                if interactive:
                    print 'GAME OVER: {} won!\n'.format(winner)
                break

            if interactive:
                raw_input('Press any key to continue...')

        if interactive:
            print 'GAME OVER: draw.\n'