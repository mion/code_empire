class OutOfBoundsError(Exception):
    def __init__(self, x, y):
        self.value = 'point ({}, {}) is out of bounds'.format(x, y)

    def __str__(self):
        return repr(self.value)

class InvalidPlayerError(Exception):
    def __init__(self, player):
        self.value = 'invalid player "{}"'.format(player)

    def __str__(self):
        return repr(self.value)