from util.dice import Dice
from util.point import Point
from model.attack import AttackResult


class Creature:
    ID_COUNTER = 0

    def __init__(self, name, player=None, level=1, position=None):
        self.id = Creature.ID_COUNTER
        Creature.ID_COUNTER += 1

        self.name = name
        self.player = player
        self.position = position

        self.level        = level
        self.max_life     = 100*level
        self.attack_power = 25*level
        self.defense      = 5*level
        
        self.life = self.max_life
        self.experience   = 0
        self.view_range   = 3
        self.attack_range = 1
        self.accuracy     = 0.90
        self.dodge        = 0.5

        self.memory = {}

    def __str__(self):
        return 'c'

    def display(self):
        print "* {}'s {}\n+- id: {}\n+- life: {}\n+- pos: {}\n".format(self.player, self.name, self.id, self.life, self.position)

    def experience_for_level(self, n):
        return 100*n

    def level_for_experience(self, experience):
        return self.experience/100

    def experience_worth(self):
        return self.level*10

    def gain_kill_experience(self, target):
        self.experience += target.experience_worth()
        self.level = self.level_for_experience(self.experience)

    def in_attack_range(self, point):
        return self.position.distance_to(point) <= self.attack_range

    def deal_damage(self, target):
        target.life -= (self.attack_power - target.defense)

    def hit_chance(self, target):
        return self.accuracy - target.dodge

    def alive(self):
        return self.life > 0

    def attack(self, target):
        if not target.alive():
            return AttackResult.DEAD
        if not self.in_attack_range(target.position):
            return AttackResult.NOT_IN_RANGE

        successful_hit = Dice.roll() < self.hit_chance(target)

        if successful_hit:
            self.deal_damage(target)

            if target.alive():
                return AttackResult.HIT
            else:
                self.gain_kill_experience(target)
                return AttackResult.KILLED
        else:
            return AttackResult.MISS

    def think(self, info):
        memory = self.memory

        if 'target_id' in memory:
            #target = info['creatures'][]
            creature = None
            if creature and not creature.alive():
                # Dead target
                del memory['target_id']
            else:
                # Attack a target
                for c in info['creatures']:
                    if c['id'] == memory['target_id']:
                        memory['target_x'] = c['x']
                        memory['target_y'] = c['y']
                        break

                if self.in_attack_range(Point(memory['target_x'], memory['target_y'])):
                    return {'action': 'attack', 'target_x': memory['target_x'], 'target_y': memory['target_y']}
                else:
                    dx, dy = self.position.dx_dy(Point(memory['target_x'], memory['target_y']))
                    return {'action': 'move', 'dx': dx, 'dy': dy}
        
        # Wander
        dx = Dice.roll(2) - 1
        dy = Dice.roll(2) - 1

        for c in info['creatures']:
            if c['player'] != self.player:
                memory['target_id'] = c['id']
                memory['target_x'] = c['x']
                memory['target_y'] = c['y']
                dx, dy = self.position.dx_dy(Point(c['x'], c['y']))

        return {'action': 'move', 'dx': dx, 'dy': dy}
