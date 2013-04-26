import unittest
from model.creature import Creature


class CreatureTest(unittest.TestCase):
	def setUp(self):
		self.creature1 = Creature(name='Creature1', 
								  player='Player1', 
								  level=1, 
								  position=Point(0, 0))
		self.creature1 = Creature(name='Creature2', 
								  player='Player2', 
								  level=1, 
								  position=Point(1, 0))

	def test_attack(self):
		self.creature1.accuracy = 1.0
		self.creature2.dodge = 0.0

		for i in range(self.creature2.life/self.creature1.damage_dealt(self.creature2)):
			self.creature1.attack(self.creature2)

		self.assertTrue(False, self.creature2.alive())


if __name__ == '__main__':
	unittest.main()
	