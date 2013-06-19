# TODO's

##### High

- Performance refactor: use just use one file for communication (instead of opening and closing), Unix-style!
- Create a "move_to" creature action that implements A* (movement with path finding).

##### Medium

- Create some unit/func tests for the game controller (simulate a whole match).
- Create a class that handles winning, losing and drawing criteria.

##### Low

- Refactor: creature.py - rename 'position' to 'pos'.
- Create a class Direction < Point, with x and y in range [1, -1] and constants NORTH, SOUTH, etc.
