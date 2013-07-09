# TODO's

##### High

- Speed: calling a shell script each time involves starting a process which is slow. Maybe keep a Python/Ruby/Node/etc process running would greatly improve performance.
- Security: review all the controllers (even though matches will run inside an isolated Linux container, we're still "running client code on the server" and bad things could happen).
- Speed: use just use one file for communication (instead of opening and closing), Unix-style!
- Maybe?: use Protocol buffers (https://code.google.com/p/protobuf/).
- Gameplay: create a "move_to" creature action that implements A* (movement with path finding).
- Refactor: extract response handling behavior from World model (rename the current World controller to "Game" controller).

##### Medium

- Refactor: use keyword arguments when calling constructors.
- Tests: create some unit/func tests for the game controller (simulate a whole match).
- Refactor: create a class that handles winning, losing and drawing criteria.

##### Low

- Refactor: creature.py - rename 'position' to 'pos'.
- Refactor: create a class Direction < Point, with x and y in range [1, -1] and constants NORTH, SOUTH, etc.
