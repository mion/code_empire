import unittest

from util.point import Point
from model.resource import Resource
from model.creature import Creature
from model.creature import AttackResult
from model.creature import GatherResult


def suite():
    combat_tests = unittest.TestLoader().loadTestsFromTestCase(CombatTestCase)
    resource_tests = unittest.TestLoader().loadTestsFromTestCase(ResourceTestCase)
    return unittest.TestSuite([combat_tests, resource_tests])


class CombatTestCase(unittest.TestCase):
    def setUp(self):
        self.attacker = Creature(name="attacker", player="player_1", level=1, position=Point(0, 0))
        self.defender = Creature(name="defender", player="player_2", level=1, position=Point(1, 0))

    def test_attack_hit(self):
        self.attacker.accuracy = 1.0
        self.defender.dodge = 0.0

        attack_result = self.attacker.attack(self.defender)

        self.assertEqual(AttackResult.HIT, attack_result)
        self.assertTrue(self.defender.life < self.defender.max_life)

    def test_attack_missed(self):
        self.attacker.accuracy = 0.0

        attack_result = self.attacker.attack(self.defender)

        self.assertEqual(AttackResult.MISS, attack_result)
        self.assertTrue(self.defender.life == self.defender.max_life)


class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.creature = Creature(name="creature_1", player="player_1", level=1, position=Point(0, 0))
        self.resource = Resource(name="resource_1", gold_amount=100, gold_flux=10)

    def test_gather_success(self):
        gather_result = self.creature.gather(self.resource)

        self.assertEqual(GatherResult.SUCCESS, gather_result)
        self.assertGreater(self.creature.gold_carried, 0)

    def test_gather_full(self):
        self.creature.gold_carried = self.creature.max_gold_carried

        gather_result = self.creature.gather(self.resource)

        self.assertEqual(GatherResult.FULL, gather_result)
        self.assertEqual(self.creature.gold_carried, self.creature.max_gold_carried)

    def test_gather_capped(self):
        self.creature.gold_carried = self.creature.max_gold_carried - self.resource.gold_flux
        gather_result = self.creature.gather(self.resource)

        self.assertEqual(GatherResult.CAPPED, gather_result)
        self.assertEqual(self.creature.gold_carried, self.creature.max_gold_carried)

    def test_gather_depleted(self):
        self.resource.gold_amount = 0

        gather_result = self.creature.gather(self.resource)

        self.assertEqual(GatherResult.DEPLETED, gather_result)
        self.assertEqual(0, self.creature.gold_carried)


if __name__ == '__main__':
    unittest.main()
