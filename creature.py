from dice import Dice
from attack import AttackResult

class Creature:
    def __init__(self, name, level, position):
        self.name = name
        self.level = level
        self.position = position
        self.set_stats(level)

    def __str__(self):
        return 'c'

    def set_stats(self, level):
        self.life = 100
        self.attack_range = 1
        self.attack_power = 25
        self.defense = 5
        self.accuracy = 0.90
        self.dodge = 0.5

    def in_attack_range(self, target):
        return self.position.distance_to(target.position) <= self.attack_range

    def deal_damage(self, target):
        target.life -= (self.attack_power - target.defense)

    def hit_chance(self, target):
        return self.accuracy - target.dodge

    def alive(self):
        return self.life > 0

    def attack(self, target):
        if not self.in_attack_range(target):
            return AttackResult.NOT_IN_RANGE

        successful_hit = Dice.roll() < self.hit_chance(target)

        if successful_hit:
            self.deal_damage(target)
            return AttackResult.HIT if target.alive() else AttackResult.KILLED
        else:
            return AttackResult.MISS