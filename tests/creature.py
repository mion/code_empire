import unittest
from model.creature import Creature
from util.point import Point


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

        self.assertTrue(self.blue_creatures[0].life < self.blue_creatures[0].max_life)


if __name__ == '__main__':
    unittest.main()