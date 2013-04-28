#!./venv/bin/python
# from model.world import World
# from view.terminal import Terminal
from controller.game import Game

if __name__ == '__main__':
    new_game = Game('mion', 'CPU')
    new_game.start()
    # red_team = 'mion'
    # blue_team = 'cpu'

    # world = World(red_team, blue_team)
    # terminal = Terminal(world)

    # for i in range(500):
    #   terminal.display(i + 1)
      
    #   winner = world.update()
      
    #   if winner:
    #     print 'GAME OVER: {} won!\n'.format(winner)
    #     break

    #   raw_input('Press any key to continue...')

    # print 'GAME OVER: draw.\n'