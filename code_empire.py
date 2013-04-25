import world

if __name__ == '__main__':
    red_team = 'mion'
    blue_team = 'rob_pike'

    world = world.World(red_team, blue_team)

    for i in range(500):
      world.display(i+1)
      
      if not world.update():
        break

      raw_input('Press any key to continue...')

    print 'Game Over'