#!./venv/bin/python
from game.controllers.world import World

if __name__ == '__main__':
    new_game = World('red', 'blue')
    winner = new_game.play()
    
    if winner:
        print 'GAME OVER: {} won!'.format(winner)
    else:
        print 'GAME OVER: draw.'
