#!./venv/bin/python
import argparse
import logging
import time

import game.controllers as controllers


def timestamp():
    return time.strftime("%d-%m-%Y-%H%M%S", time.gmtime())

def setup_logging():
    lg = logging.getLogger('code_empire')
    log_fn = 'game_{}.log'.format(timestamp())
    logging.basicConfig(filename=log_fn, format='[%(levelname)s] %(name)s\n\t\t-- %(message)s\n', level=logging.DEBUG)
    lg.setLevel(logging.DEBUG)
    return lg
 
def new_game(players, inter):
    lg = setup_logging()
    lg.info('starting new game (interactive: {}), players: {}'.format(inter, players))

    game = controllers.Game(players[0], players[1])
    result = game.play(interactive=inter)

    lg.info('game over, winner: {}'.format(result.winner))   
    print result

def new_game_interactive(players):
    new_game(players, True)

def new_game_result_only(players):
    new_game(players, False)


if __name__ == '__main__':
    setup_logging()

    parser = argparse.ArgumentParser(description='The epic programming game -- this program plays an entire CodeEmpire match between two players.')
    parser.add_argument('players', metavar='P', 
                        type=str, nargs=2, 
                        help='the contestants for this battle')
    parser.add_argument('--interactive', dest='new_game', action='store_const',
                        const=new_game_interactive, default=new_game_result_only,
                        help='view the gameplay step by step (default: just output the match result)')
    args = parser.parse_args()

    print 'Playing match, please wait...'
    args.new_game(args.players)
