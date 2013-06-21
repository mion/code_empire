# TODO's

##### High

- Security: review all the controllers (even though matches run inside an isolated Linux container, we're still "running client code on the server" and bad things could happen).
- Performance refactor: use just use one file for communication (instead of opening and closing), Unix-style!
- Create a "move_to" creature action that implements A* (movement with path finding).
- Refactor: extract response handling behavior from World model (rename the current World controller to "Game" controller).

##### Medium

- Refactor: use keyword arguments when calling constructors.
- Create some unit/func tests for the game controller (simulate a whole match).
- Create a class that handles winning, losing and drawing criteria.

##### Low

- Refactor: creature.py - rename 'position' to 'pos'.
- Create a class Direction < Point, with x and y in range [1, -1] and constants NORTH, SOUTH, etc.
