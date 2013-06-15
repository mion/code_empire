import unittest

from game.utils import Point
from game.models import World, Creature, Resource


class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.world = World('red', 'blue')

    def test_generate(self):
        import random

        self.world.generate(random)
        self.assertGreater(len(self.world.creatures), 0)

    def test_insert_creature(self):
        c = Creature(name='creature', player='red', position=Point(0, 0))
        count = len(self.world.creatures)

        self.world.insert_creature(c)

        self.assertGreater(len(self.world.creatures), count)
        self.assertEqual(c, self.world.get_entity_at(c.position.x, 
                                                     c.position.y))
        self.assertEqual(c, self.world.creatures[c.id])

    def test_move_creature(self):
        c = Creature(name='creature', player='red', position=Point(0, 0))
        self.world.insert_creature(c)

        self.assertTrue(self.world.move_creature(c, 1, 1))
        self.assertEqual(Point(1, 1), c.position)
        self.assertEqual(c, self.world.get_entity_at(1, 1))

    def test_move_creature_out_of_bounds(self):
        c = Creature(name='creature', player='red', position=Point(0, 0))
        self.world.insert_creature(c)

        self.assertFalse(self.world.move_creature(c, -1, 1))
        self.assertEqual(Point(0, 0), c.position)
        self.assertEqual(c, self.world.get_entity_at(0, 0))

    @unittest.skip("[world.py] Not ready yet.")
    def test_generate_map(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()