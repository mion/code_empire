#!./venv/bin/python
import time

from game.controllers import World


def timestamp():
    return time.strftime("%d-%m-%Y-%H%M%S", time.gmtime())

def setup_logging():
    import logging

    log_fn = 'game_{}.log'.format(timestamp())
    logging.basicConfig(filename=log_fn, format='[%(levelname)s] %(name)s\n\t\t-- %(message)s\n', level=logging.DEBUG)
    logger = logging.getLogger('code_empire')
    logger.setLevel(logging.DEBUG)
    logger.info('starting new game')

if __name__ == '__main__':
    setup_logging()

    new_game = World('red', 'blue')
    winner = new_game.play()
    
    if winner:
        print 'GAME OVER: {} won!'.format(winner)
    else:
        print 'GAME OVER: draw.'
