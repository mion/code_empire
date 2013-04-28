import unittest
from util.point import Point
from model.creature import Creature
from model.attack import AttackResult


class TestCreature(unittest.TestCase):
    def setUp(self):
        self.red_creatures = [
            Creature(name="red_creature_0", player="red", level=1, position=Point(0, 0)),
            Creature(name="red_creature_1", player="red", level=1, position=Point(0, 1))
        ]
        self.blue_creatures = [
            Creature(name="blue_creature_0", player="blue", level=1, position=Point(1, 0)),
            Creature(name="blue_creature_1", player="blue", level=1, position=Point(1, 1))
        ]

    def test_attack_hit(self):
        self.red_creatures[0].accuracy = 1.0
        self.blue_creatures[0].dodge = 0.0

        attack_result = self.red_creatures[0].attack(self.blue_creatures[0])

        self.assertEqual(AttackResult.HIT, attack_result)
        self.assertTrue(self.blue_creatures[0].life < self.blue_creatures[0].max_life)

    def test_attack_missed(self):
        self.red_creatures[0].accuracy = 0.0

        attack_result = self.red_creatures[0].attack(self.blue_creatures[0])

        self.assertEqual(AttackResult.MISS, attack_result)
        self.assertTrue(self.blue_creatures[0].life == self.blue_creatures[0].max_life)


if __name__ == '__main__':
    unittest.main()