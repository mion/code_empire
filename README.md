Code Empire
-----------
*Work In Progress*: v1.0 will be posted on HN as soon as it's playable.<br>

## What is it?
A programming game in the likes of "Age of Empires" to test your skills.<br>
In **Code Empire**, you are to implement the AI code that controls a small army seeking to destroy the enemy forces.<br>
The game is *language agnostic*, meaning you're free to write the AI code in any language you want.

## Rules
Each player has a *fortress* and several *creatures*.<br>
* Creatures can act both as peons, gathering gold from *resources* that are scattered around the map, as well as military units, attacking enemy creatures and fortresses.<br>
* Fortresses can create other creatures (at the cost of *gold*) and also attack nearby enemy units. They're much stronger than normal creatures.

The *objective* is to destroy the other player's fortress.

## How to play?
1. Fork this repo
2. Create a directory with your Github username inside ```ai```` (you can find a few example AIs in there).
3. That's it! You're now playing Code Empire.

Well, not actually. The server looks for the latest commits on your master branch


TODOs
-----
## High
- Refactor: creature.py, fortress.py, resource.py - create an Entity class from which they inherit ID, position, etc.
- Performance refactor: game.py - use just use one file for communication (instead of opening and closing), Unix-style!
## Normal
- Create unit/func tests for game controller.
- Create unit tests for world.
- Refactor: world.py, tilemap.py - change method prototypes to use Point instead of x and y.
- Refactor: world.py - create a method for each action and handle the message in a creature controller class. Put them in a Controller!
## Low
- Refactor: world.py - create a class that handles winning, losing and drawing criteria.
- Refactor: creature.py - rename 'position' to 'pos'.
- Creature a class Direction < Point, with x and y in range [1, -1] and constants NORTH, SOUTH, etc.
