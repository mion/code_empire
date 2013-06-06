Code Empire - Episode 1.0: Attack of the Languages
-----------
*Code Empire* is a game where programmers clash by writing AI code in their favorite language, seeking fame, fortune and a chance to honour their respective communities.<br>

![Art by emkun.devianart.com](http://fc07.deviantart.net/fs70/f/2011/196/0/b/battle_by_emkun-d3s71ke.png "Art by emkun.devianart.com")

## What is it?
A strategy game in the likes of Warcraft/Age of Empires, except you don't move the pieces with your mouse: you write code to do it for you.<br>
In *Code Empire*, you are to implement the AI that controls a small army seeking to destroy the enemy forces.<br>
The game is **language agnostic**, meaning you're free to write the AI code in any language you want.<br>

## Rules
Each player has a **fortress** and several *creatures*.<br>
* After each round, you're granted an additional amount of gold based on _how fast your code runs_.
* Fortresses can create creatures (at the cost of **gold**) and also attack nearby enemy units. 
* Creatures can be customized in order to create classes of units with different responsabilities. Two common classes are peons, units that gather gold from **resources** that are scattered around the map, and military units that attack enemy creatures and fortresses.<br>

The main objective is to **destroy the other player's fortress**.

## How to play?
Currently, the game is only halfway finished and not ready to be played.<br>
It shouldn't take me too long to get a version 1.0 out and running on a server, but if you like the idea and want to speed up things, consider giving this repo *a star*.<br>
Thanks :) That should boost my morale a bit. Now if you feel like to, read on to understand the game rules.<br>
Any ideas are welcome at this point, so feel free to open an issue or something!

## Gameplay
Each round, the ```creature.sh``` script in your directory is called for every one of your creatures.<br>
The script receives a JSON (serialized string) with information available to that particular creature. Your code will then return another JSON with the action that should be taken by the creature.<br>
The same goes for your ```fortress.sh``` script.<br>

##### Fortress
The AI for the fortress is pretty straightforward. Each round it should probably start by looking for nearby enemy creatures and attack the stronger one.<br>
Most rounds, however, it should decide whether or not to create more creatures and mainly, how the creature should be.<br>
You can create custom creatures by tinkering with these parameters:
- Attack range
- Attack power
- Defence rating
- Dodge
- Accuracy

Some parameters cost more gold than others. You could create "an archer", for instance, by increasing a creature's attack range and accuracy, while decreasing the defense rating.

##### Creature
The creature

---

### TODOs

##### High
- Refactor: creature.py, fortress.py, resource.py - create an Entity class from which they inherit ID, position, etc.
- Performance refactor: game.py - use just use one file for communication (instead of opening and closing), Unix-style!

#####Normal
- Create unit/func tests for game controller.
- Create unit tests for world.
- Refactor: world.py, tilemap.py - change method prototypes to use Point instead of x and y.
- Refactor: world.py - create a method for each action and handle the message in a creature controller class. Put them in a Controller!

##### Low
- Refactor: world.py - create a class that handles winning, losing and drawing criteria.
- Refactor: creature.py - rename 'position' to 'pos'.
- Creature a class Direction < Point, with x and y in range [1, -1] and constants NORTH, SOUTH, etc.
