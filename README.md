Code Empire - Episode 1.0: Attack of the Languages
-----------
*Code Empire* is a game where programmers clash by writing AI code in their favorite language, seeking fame, fortune and a chance to honour their respective communities.<br>
May the best hacker win!

**Work In Progress**: v1.0 will be posted on HN as soon as it's playable.<br>

![Art by emkun.devianart.com](http://fc07.deviantart.net/fs70/f/2011/196/0/b/battle_by_emkun-d3s71ke.png "Art by emkun.devianart.com")

## What is it?
A programming game in the likes of "Age of Empires", except you don't move the pieces with your mouse; rather, you write code to do it for you.<br>
In *Code Empire*, you are to implement the AI that controls a small army seeking to destroy the enemy forces.<br>
The game is **language agnostic**, meaning you're free to write the AI code in any language you want.

## Rules
Each player has a **fortress** and several *creatures*.<br>
* Creatures can act both as peons, gathering gold from **resources** that are scattered around the map, as well as military units, attacking enemy creatures and fortresses.<br>
* Fortresses can create other creatures (at the cost of **gold**) and also attack nearby enemy units. They're much stronger than normal creatures.
* You're also granted an additional amount of gold each round, based on how fast your code runs.

The main objective is to **destroy the other player's fortress**.

## How to play?
1. Fork this repo
2. Create a directory with **your Github username** inside ```ai```.
3. Write your AI, commit and push your changes. A few example AIs are provided for you.
4. That's it! You're now playing Code Empire.

A cronjob looks for the latest commit on your *master* branch and automatically updates it on the game server (all other branches are ignored).

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
