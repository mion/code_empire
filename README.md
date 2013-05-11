Code Empire Server
------------------
A game to test your programming skills.<br>
This is the server code.

## How to play?
All you need to do is fork this repo and you're automatically playing.

TASK LIST
------------------
## High
[ ] Refactor: creature.py, fortress.py, resource.py - create an Entity class from which they inherit ID, position, etc.
[ ] Performance refactor: game.py - use just use one file for communication (instead of opening and closing), Unix-style!
## Normal
[ ] Create unit tests for game controller.
[ ] Create unit tests for world.
[ ] Refactor: world.py, tilemap.py - change method prototypes to use Point instead of x and y.
## Low
[ ] Refactor: world.py - create a method for each action and handle the message in a creature controller class.
[ ] Refactor: world.py - create a class that handles winning, losing and drawing criteria.
[ ] Refactor: creature.py - change 'position' to 'pos'.
[ ] Creature a class Direction that is a Point, but with x and y in range [1, -1], with init NORTH, SOUTH, etc.
## Done :)
[x] Refactor: attack.py - put it back in the Creature module.
[x] Add more UnitTests.