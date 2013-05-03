#!./venv/bin/python
from controller.game import Game

if __name__ == '__main__':
    new_game = Game('red', 'blue')
    winner = new_game.start()
    
    if winner:
        print 'GAME OVER: {} won!'.format(winner)
    else:
        print 'GAME OVER: draw.'