# -*- coding: utf-8 -*-

"""
game.controllers
~~~~~~~~~~~~~~~~~~~

Controllers handle the exchange of message (input/output) that go "in and out"
of models.

"""

import sys
import subprocess
import json
import md5
import random

import models
import views

class Game(object):
    MAX_ROUNDS = 500
    TEMP_DIR = 'temp/'

    def __init__(self, red_player, blue_player):
        self.world = models.World(red_player, blue_player)
        self.world.generate(random)
        self.terminal = views.Terminal(self.world)

    def random_hash(self):
        return md5.new(str(random.random())).hexdigest()

    def call_think(self, player, info_filename, response_filename):
        """
        Calls the 'think.sh' script for a given player.
        """
        try:
            # TODO: security issue with check_output - possibly malicious player name?
            subprocess.check_output(["./ai/{}/think.sh '{}' '{}'".format(player, info_filename, response_filename)], shell=True)
        except subprocess.CalledProcessError, e:
            print '\nAn error occurred when running think.sh: ' + str(e)
            sys.exit(1)

    def exchange_message(self, player, info):
        """
        Exchange a message using randomically named JSON files.
        """
        # TODO: use Unix temp files (Python's tempfile module)
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

    def play(self, interactive=False):
        """
        Play a whole match.
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
                return MatchResult(winner)

            if interactive:
                raw_input('Press any key to continue...')

        return MatchResult(None)


class MatchResult(object):
    """The end result for a match."""
    def __init__(self, winner):
        self.winner = winner
        
    def __str__(self):
        if self.winner:
            return "GAME OVER - Winner: {}".format(self.winner)
        else:
            return "GAME OVER - Draw"


# TODO: puts these in a "messages" module.
class Message(object):
    """Message exchanged between the player's AI and the world."""
    def __init__(self, body):
        self.body = body
        
    def to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.body, f)

    @classmethod
    def from_json(self, filename):
        with open(filename, 'r') as f: #FIXME: check if file is there
            body = json.load(f)

        return Message(body=body)
