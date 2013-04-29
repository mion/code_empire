import sys
import subprocess
import json
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
                    print 'An error occurred when running think.sh: ' + str(e)
                    sys.exit(1)

            winner = self.world.update()

            if winner:
                if interactive:
                    print 'GAME OVER: {} won!\n'.format(winner)
                break

            if interactive:
                raw_input('Press any key to continue...')

        if interactive:
            print 'GAME OVER: draw.\n'