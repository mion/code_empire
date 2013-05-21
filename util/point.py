class Point(object):
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
    min, max -- Points denoting the lower (min) and upper (max) bounds for x and y.
                NOTE: lower.x <= x < upper.x (same for y)
    count -- The number of points to generate. If count is 1, returns a single point.
    """
    if count > 1:
      points = []

      x_ary = [i for i in range(lower.x, upper.x)]
      y_ary = [i for i in range(lower.y, upper.y)]

      random.shuffle(x_ary)
      random.shuffle(y_ary)

      for x, y in zip(x_ary, y_ary):
        points.append(Point(x, y))

      return points
    else:
      return Point(random.randrange(lower.x, upper.x), random.randrange(lower.y, upper.y))
