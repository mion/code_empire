from random import random


class Dice:
  @staticmethod
  def roll(n=None):
    if n:
      return int((n+1)*random())
    else:
      return random()