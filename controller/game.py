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
    TEMP_DIR = 'temp/'

    def __init__(self, red_player, blue_player):
        self.world = World(red_player, blue_player)
        self.terminal = Terminal(self.world)

    def random_hash(self):
        return md5.new(str(random())).hexdigest()

    def call_think(self, player, info_filename, response_filename):
        """
        Calls the 'think.sh' script for a given player.
        """
        try:
            # TODO: security issue with check_output (possibly malicious player name?)
            subprocess.check_output(["./ai/{}/think.sh '{}' '{}'".format(player, info_filename, response_filename)], shell=True)
        except subprocess.CalledProcessError, e:
            print '\nAn error occurred when running think.sh: ' + str(e)
            sys.exit(1)

    def exchange_message(self, player, info):
        """
        Exchange a message using randomically named JSON files.
        """
        info_filename = Game.TEMP_DIR + self.random_hash()
        response_filename = Game.TEMP_DIR + self.random_hash()

        with open(info_filename, 'w') as f:
            json.dump(info, f)

        self.call_think(player, info_filename, response_filename)

        with open(response_filename, 'r') as f: #FIXME: check if file is there
            response_json = json.load(f)

        return response_json

    def clear_temp_dir(self):
        import os
        os.system('rm ' + Game.TEMP_DIR + '*')

    def start(self, interactive=True):
        """
        Start and play a whole match.
        """
        if interactive:
                self.terminal.display(0)

        for i in range(Game.MAX_ROUNDS):
            creatures = self.world.creatures

            for id in creatures:
                creature = creatures[id]
                player = creature.player

                # Gather available info for that creature
                info = self.world.gather_creature_info(creatures[id])
                # Send that info to the AI, get the response
                response = self.exchange_message(player, info)
                # World handles the player's AI commands
                self.world.handle_creature_response(response, creatures[id])

                # Clear the temp directory (used for message passing)
                self.clear_temp_dir()
                
            if interactive:
                self.terminal.display(i + 1)

            winner = self.world.update()

            if winner:
                return winner

            if interactive:
                raw_input('Press any key to continue...')

        return None