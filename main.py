from Tkinter import *
from random import random


class Dice:
  @staticmethod
  def roll(n=None):
    if n:
      return int((n+1)*random())
    else:
      return random()

class AttackResult:
  KILLED = 'killed'
  HIT = 'hit'
  MISS = 'miss'
  NOT_IN_RANGE = 'not in range'


class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def distance_to(self, point):
    return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

  def dx_dy(self, point):
    dx = point.x - self.x
    if dx != 0:
      dx /= abs(dx)
    dy = point.y - self.y
    if dy != 0:
      dy /= abs(dy)
    return (dx, dy)


class Creature:
  def __init__(self, name, level, position, player_name):
    self.name = name
    self.experience = 0
    self.position = position
    self.player_name = player_name
    self.set_stats(level)
    self.memory = {}

  def set_stats(self, level):
    self.level = level
    self.life = 100*level
    self.view_range = 3
    self.attack_range = 1
    self.attack_power = 20*level
    self.defense = 5*level
    self.accuracy = 0.85
    self.dodge = 0.15

  def experience_for_level(self, n):
    return 100*n

  def level_for_experience(self, experience):
    return self.experience/100

  def hit_chance(self, target):
    return self.accuracy - target.dodge

  def damage_dealt(self, target):
    return self.attack_power - target.defense

  def experience_worth(self, target):
    return target.level*10

  def in_attack_range(self, point):
    return self.position.distance_to(point) <= self.attack_range

  def deal_damage(self, target):
    damage = self.damage_dealt(target)
    target.life -= damage
    return damage

  def gain_kill_experience(self, target):
    self.experience += self.experience_worth(target)
    self.level = self.level_for_experience(self.experience)

  def alive(self):
    return self.life > 0

  def resurrect(self):
    self.life = 100
    self.experience = 0

  def attack(self, target):
    if not self.in_attack_range(target.position):
      return AttackResult.NOT_IN_RANGE

    successful_hit = self.hit_chance(target) > Dice.roll()
    if successful_hit:
      self.deal_damage(target)
      if target.life <= 0:
        self.gain_kill_experience(target)
        return AttackResult.KILLED
      else:
        return AttackResult.HIT
    else:
      return AttackResult.MISS

  def think(self, info):
    memory = self.memory

    if 'target' in memory:
      for c in info['creatures']:
        if c['name'] == memory['target']:
          memory['target_x'] = c['x']
          memory['target_y'] = c['y']
          print 'Updating target position...'
          break

      print 'Checking attack range...'
      if self.in_attack_range(Point(memory['target_x'], memory['target_y'])):
        print 'OK'

        return {'action': 'attack', 'target_x': memory['target_x'], 'target_y': memory['target_y']}
      else:
        print 'False'
        dx, dy = self.position.dx_dy(Point(memory['target_x'], memory['target_y']))
  
        return {'action': 'move', 'dx': dx, 'dy': dy}
    else:
      print 'No target.'
      dx = Dice.roll(2) - 1
      dy = Dice.roll(2) - 1

      for c in info['creatures']:
        if c['player_name'] != self.player_name:
          print '{} found a target: {} ({}, {})'.format(self.name, c['name'], c['x'], c['y'])
          memory['target'] = c['name']
          memory['target_x'] = c['x']
          memory['target_y'] = c['y']
          dx, dy = self.position.dx_dy(Point(c['x'], c['y']))
          print 'Moving dx: {}, dy: {}'.format(dx, dy)

      return {'action': 'move', 'dx': dx, 'dy': dy}


class CombatSimulator(object):
  """Simulates combat between two creatures."""
  def __init__(self, creature1, creature2):
    self.creature1 = creature1
    self.creature2 = creature2

  def output_attack_result(self, attacker, defendant, attack_result):
    print '- {} attacks {}: {}'.format(attacker.name, defendant.name, attack_result)

  def run(self, max_rounds, output=False):
    for i in range(max_rounds):
      if output: 
        print '--- Round {}\n{}\'s life: {}\n{}\'s life: {}\n'.format(i, self.creature1.name, self.creature1.life, self.creature2.name, self.creature2.life)

      result1 = self.creature1.attack(self.creature2)
      result2 = self.creature2.attack(self.creature1)

      if output:
        self.output_attack_result(self.creature1, self.creature2, result1)
        self.output_attack_result(self.creature2, self.creature1, result2)

      if not self.creature1.alive() and self.creature2.alive():
        if output:
          print '{} won!\n\n'.format(self.creature2.name)

        return (self.creature2, i)
      elif not self.creature2.alive() and self.creature1.alive():
        if output:
          print '{} won!\n\n'.format(self.creature1.name)

        return (self.creature1, i)
      elif not self.creature1.alive() and not self.creature2.alive():
        break

    if output:
      print 'Draw!\n\n'

    return (None, i)

  def run_statistics(self, times):
    statistics = {}
    for c in [self.creature1, self.creature2, None]:
      statistics[c] = {'wins': 0, 'rounds': 0}

    for i in range(times):
      self.creature1.resurrect()
      self.creature2.resurrect()
      result_tuple = self.run(50)
      winner = result_tuple[0]
      rounds = result_tuple[1]
      statistics[winner]['wins'] += 1
      statistics[winner]['rounds'] += rounds

    s = "SIMULATION RESULT:\n{}\t{}%.\n{}\t{}%.\nDraw\t{}%.\n"
    print s.format(self.creature1.name,
                   (1.0*statistics[self.creature1]['wins']/times)*100.0,
                   self.creature2.name,
                   (1.0*statistics[self.creature2]['wins']/times)*100.0,
                   (1.0*statistics[None]['wins']/times)*100.0)


class World(object):
  """World controls all the objects"""
  def __init__(self, size):
    self.player_data = {}
    self.players = []
    self.creatures = []
    self.size = size
    self.tiles = [[None for i in range(size)] for j in range(size)]

  def insert_player(self, player_name):
    self.players.append(player_name)
    self.player_data[player_name] = {"creatures": [], "gold": 0}

  def insert_creature(self, c):
    self.creatures.append(c)
    self.player_data[c.player_name]['creatures'].append(c)
    self.tiles[c.position.x][c.position.y] = c

  def move_creature(self, c, dx, dy):
    to_x = c.position.x + dx
    to_y = c.position.y + dy

    if self.in_bounds(to_x, to_y) and self.tiles[to_x][to_y] == None:
      self.tiles[c.position.x][c.position.y] = None
      self.tiles[to_x][to_y] = c
      c.position.x = to_x
      c.position.y = to_y

      return True
    else:
      return False

  def standing_players(self):
    return filter(lambda player: self.player_data[player]['creatures'] > 0, self.players)

  def in_bounds(self, x, y):
    return (0 <= x < self.size) and (0 <= y < self.size)

  def info_for_creature(self, creature):
    info = {'creatures': []}

    x0 = creature.position.x - creature.view_range
    xf = creature.position.x + creature.view_range
    y0 = creature.position.y - creature.view_range
    yf = creature.position.y + creature.view_range

    for x in range(x0, xf + 1): # there's probably a smarter way of doing this
      for y in range(y0, yf + 1):
        if self.in_bounds(x, y) and self.tiles[x][y]:
          c = self.tiles[x][y]
          creature_info = {
            'name': c.name,
            'level': c.level,
            'life': c.life,
            'player_name': c.player_name,
            'x': x,
            'y': y
          }
          info['creatures'].append(creature_info)

    return info

  def update(self):
    for creature in self.creatures:
      # TODO: remove dead creatures
      # if not creature.alive():
      #   del self.creatures[creature]
      #   continue

      info = self.info_for_creature(creature)
      resp = creature.think(info)

      if resp['action'] == 'move':
        dx, dy = 0, 0
        if 'dx' in resp: dx = resp['dx']
        if 'dy' in resp: dy = resp['dy']
        self.move_creature(creature, dx, dy)
      if resp['action'] == 'attack':
        print 'Attacking!'
        target_x, target_y = 0, 0
        if 'target_x' in resp: 
          target_x = resp['target_x']
        if 'target_y' in resp: 
          target_y = resp['target_y']
        target_creature = self.tiles[target_x][target_y]
        creature.attack(target_creature)

    survivors = self.standing_players()
    if len(survivors) <= 1:
      return True
    else:
      return False

  def display(self):
    print 'World:'
    for i in range(self.size):
      row = ''
      for j in range(self.size):
        creature = self.tiles[i][j]
        if creature:
          row += '[{}]'.format(creature.player_name[0])
        else:
          row += '[ ]'
      print row

    print 'Creatures'
    print 'Name\Life\tX\tY'
    for c in self.creatures:
      print '{}\t{}\t{}\t{}'.format(c.name, c.life, c.position.x, c.position.y)
    print '-'*10

if __name__ == '__main__':
  # c1 = Creature('Orc', 1, Point(0, 0))
  # c2 = Creature('Troll', 1, Point(0, 0))
  # cs = CombatSimulator(c1, c2)
  # cs.run_statistics(5000)
  world = World(10)
  world.insert_player('A')
  world.insert_player('B')

  a1 = Creature('Orc 1', 1, Point(0, 0), 'A')
  a2 = Creature('Orc 2', 1, Point(1, 0), 'A')
  b1 = Creature('Troll 1', 1, Point(9, 9), 'B')
  b2 = Creature('Troll 2', 1, Point(8, 9), 'B')

  world.insert_creature(a1)
  world.insert_creature(a2)
  world.insert_creature(b1)
  world.insert_creature(b2)

  for i in range(500):
    world.display()
    if world.update():
      break
    raw_input('Press any key to continue...')

  print 'Game Over'