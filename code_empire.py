#!./venv/bin/python
import argparse
import logging
import time

import game.controllers as controllers


logger = logging.getLogger('code_empire')

def _timestamp():
    return time.strftime("%d-%m-%Y-%H%M%S", time.gmtime())

def _setup_logging():
    log_fn = 'game_{}.log'.format(_timestamp())
    logging.basicConfig(filename=log_fn, format='[%(levelname)s] %(name)s\n\t\t-- %(message)s\n', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    
def new_game_interactive(players):
    logger.info('starting new game (interactive mode), players: {}'.format(players))
    new_game = controllers.World(players[0], players[1])
    result = new_game.play(interactive=True)   
    logger.info('game over, winner: {}'.format(result.winner))   
    print result 

def new_game_result_only(players):
    logger.info('starting new game, players: {}'.format(players))
    new_game = controllers.World(players[0], players[1])
    result = new_game.play()
    logger.info('game over, winner: {}'.format(result.winner))   
    print result 


if __name__ == '__main__':
    _setup_logging()

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
