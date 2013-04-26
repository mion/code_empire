#!./venv/bin/python
from model.world import World
from view.terminal import Terminal


if __name__ == '__main__':
    red_team = 'mion'
    blue_team = 'jarvis'

    world = World(red_team, blue_team)
    terminal = Terminal(world)

    for i in range(500):
      terminal.display(i + 1)
      
      if not world.update():
        break

      raw_input('Press any key to continue...')

    print 'Game Over'