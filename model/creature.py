import random
from util.point import Point


class Creature(object):
    """
    docstring for Creature
    """

    ID_COUNTER = random.randrange(0, 101) # Add random initial ID to avoid cheating (finding the other player's creatures).

    def __init__(self, name, player=None, level=1, position=None):
        self.id = str(Creature.ID_COUNTER)
        Creature.ID_COUNTER += random.randrange(1, 101)

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

        self.gold_carried = 0
        self.max_gold_carried = 100

        self.memory = {}

    def __str__(self):
        return 'c'

    def __repr__(self):
        #print "* {}'s {}\n+- id: {}\n+- life: {}\n+- pos: {}\n".format(self.player, self.name, self.id, self.life, self.position)
        return "{} {}, life: {} [ID: {}]\n".format(self.position, self.name, self.life, self.id)

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

        successful_hit = random.random() < self.hit_chance(target)

        if successful_hit:
            self.deal_damage(target)

            if target.alive():
                return AttackResult.HIT
            else:
                self.gain_kill_experience(target)
                return AttackResult.KILLED
        else:
            return AttackResult.MISS

    def is_full(self):
        return self.gold_carried < self.max_gold_carried

    def space_left(self):
        return self.max_gold_carried - self.gold_carried

    def gather(self, resource):
        if not resource.depleted():
            if self.is_full():
                return GatherResult.FULL
            else:
                self.gold_carried += resource.gather()
                return GatherResult.SUCCESS
        else:
            return GatherResult.DEPLETED


class GatherResult(object):
    """Possible outcomes returned by a Creature's gather method."""
    SUCCESS         = 1 # Successfully gathered some resource.
    DEPLETED        = 2 # There's no more resource left.
    FULL            = 3 # Can't hold any more gold.


class AttackResult(object):
    """Possible outcomes returned by a Creature's attack method."""
    HIT             = 1 # Succesfully dealt damage to target.
    MISS            = 2 # Failed to hit target.
    KILLED          = 3 # Hit and also killed the target.
    NOT_IN_RANGE    = 4 # Target is too far.
    DEAD            = 5 # Target is already dead.