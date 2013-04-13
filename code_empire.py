import random


class AttackResult:
    KILLED = 'killed'
    HIT = 'hit'
    MISS = 'miss'
    NOT_IN_RANGE = 'not in range'

class Dice:
    @staticmethod
    def roll():
        return random.random()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

class Creature:
    def __init__(self, name, level, position):
        self.name = name
        self.level = level
        self.position = position
        self.set_stats(level)

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

class CombatSimulation:
    def __init__(self, c1, c2, max_rounds):
        self.c1 = c1
        self.c2 = c2
        self.max_rounds = max_rounds

    def run(self, output):
        c1 = self.c1
        c2 = self.c2
        for r in range(self.max_rounds):
            output('--- Round {}\n{}\' life: {}\n{}\'s life: {}\n'.format(r, c1.name, c1.life, c2.name, c2.life))
            ar1 = c1.attack(c2)
            ar2 = c2.attack(c1)

            output('{} {}\n{} {}\n\n'.format(c1.name, ar1, c2.name, ar2))

            if not c1.alive():
                output('{} won!'.format(c2.name))
                return (c2, r)
            if not c2.alive():
                output('{} won!'.format(c1.name))
                return (c1, r)

        return (None, self.max_rounds)


if __name__ == '__main__':
    simulations = 5000
    name_a = 'orc'
    name_b = 'troll'
    matches = []

    def output(s):
        return

    for i in range(simulations):
        a = Creature('orc', 1, Point(0, 0))
        b = Creature('troll', 1, Point(0, 0))
        cs = CombatSimulation(a, b, 50)
        result = cs.run(output)
        match = {'winner': result[0].name, 'rounds': result[1]}
        matches.append(match)

    a_wins = 0
    b_wins = 0
    a_rounds = 0
    b_rounds = 0
    draws = 0

    for match in matches:
        if match['winner'] == name_a:
            a_wins += 1
            a_rounds += match['rounds']
        elif match['winner'] == name_b:
            b_wins += 1
            b_rounds += match['rounds']
        else:
            draws += 1

    print 'Simulation results:\n{} won {} times\n{} won {} times\n{} draws\n'.format(name_a, a_wins, name_b, b_wins, draws)

