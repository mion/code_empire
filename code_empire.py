#!./venv/bin/python
from controller.game import Game

if __name__ == '__main__':
    new_game = Game('red', 'blue')
    new_game.start()