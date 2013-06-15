import unittest
from game.utils import Point

class PointTestCase(unittest.TestCase):
    def test_init(self):
        p1 = Point(5)
        p2 = Point(3, 5)
        p2.x = 5
        self.assertEqual(p1, p2)
