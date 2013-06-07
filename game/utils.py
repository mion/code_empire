# -*- coding: utf-8 -*-

"""
game.utils
~~~~~~~~~~~~~~~~~~~

Utility classes and functions.

"""

class Point(object): # REFACTOR: http://docs.python.org/2/library/collections.html#collections.namedtuple
  def __init__(self, x, y=None):
    self.x = x
    if y != None:
      self.y = y
    else:
      self.y = x

  def __str__(self):
    return "({}, {})".format(self.x, self.y)

  def __eq__(self, point):
    return self.x == point.x and self.y == point.y

  def distance_to(self, point):
    return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

  def dx_dy(self, point):
    dx = point.x - self.x
    if dx != 0:
      dx /= abs(dx)
    dy = point.y - self.y
    if dy != 0:
      dy /= abs(dy)
    return (dx, dy)

  @staticmethod
  def generate(random, lower, upper, count=1):
    """
    Generates unique random points.
    Returns an array of (or a single) Point.

    Keyword arguments:
    random -- An instance of Python's random object.
    lower, upper -- Points denoting the lower (min) and upper (max) bounds for x and y.
                NOTE: lower.x <= x < upper.x (same for y)
    count -- The number of points to generate. If count is 1, returns a single point.
             Note that count is actually capped by the amount of all possible points
             in the region defined by lower/upper.
    """
    if count > 1:
      points = []

      for x in range(lower.x, upper.x):
        for y in range(lower.y, upper.y):
          points.append(Point(x, y)) # REFACTOR: Not very efficient

      return random.sample(points, count)
    else:
      return Point(random.randrange(lower.x, upper.x), random.randrange(lower.y, upper.y))
