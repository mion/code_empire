Code Empire [Work In Progress]
-----------
*Code Empire* is an epic game where programmers clash by writing AI code in their favorite language.<br>

![Art by emkun.devianart.com](http://fc07.deviantart.net/fs70/f/2011/196/0/b/battle_by_emkun-d3s71ke.png "Art by emkun.devianart.com")

## What is it?

A strategy game in the likes of Warcraft/Age of Empires, except you don't move the pieces with your mouse: you write code to do it for you.<br>
The game is **language agnostic** (meaning you're free to write the AI code in any language you want) since **JSON** is used to exchange messages between the world and your bots' AI.<br>

## Rules

Each player has a **fortress** and several *creatures*.<br>
* After each round, you're granted an additional amount of gold based on _how fast your code runs_.
* Fortresses can create creatures (at the cost of **gold**) and also attack nearby enemy units. 
* Creatures can be customized (by tweeking their initial stats) in order to create different classes of units. E.g.: peons, units that gather gold from **resources** that are scattered around the map; military units that attack enemy creatures and fortresses; etc.<br>

The main objective is to **destroy the other player's fortress**.

## How to play?

##### Work in Progress

Currently, the game is only halfway finished and not ready to be played :(<br>
I'll be posting v1.0 on HackerNews pretty soon, but any support is appreciated: feel free to submit ideas, suggestions, code.<br>
If you'd like to boost my morale a bit, you could also *star the repo*! Thanks :)<br>

## Gameplay

Each round, the ```creature.sh``` script in your directory is called for every one of your creatures.<br>
The script receives a JSON with information available to that particular creature. Your code will then return another JSON with the action that should be taken by the creature.<br>
The same goes for your ```fortress.sh``` script.<br>
Eg.: A level 3 creature called "Orc" standing at (3, 5) would receive this:

    {
        'myself': {
            'name': 'Orc',
            'life': 350,
            'level': 3,
            'x': 3,
            'y': 5,
            'group': 'default'
        },
        'nearby_enemies': {
            'Troll': {
                'life': 100,
                'level': 1,
                'x': 5,
                'y': 7
            }
        },
        'nearby_allies': {}
    }

##### Fortress

Fortresses have two actions:

- Attack nearby enemy units
- Create creatures

They are much stronger than creatures and have wide attack range. Obviously, they cannot move.<br>
You can create custom creatures by tinkering with these parameters:

- Attack range
- Attack power
- Defence rating
- Dodge
- Accuracy

Some parameters cost more gold than others. You could create "an archer", for instance, by increasing a creature's attack range and accuracy, while decreasing the defense rating.<br>
You can also assign them to groups upon creation, and later on send messages to the whole group.

##### Creature

Creatures have four actions:
- Move around the map
- Attack other creatures
- Gather resources
- Return resources to a fortress

---

### Some cool ideas

- Write a HTML5 parser for battle logs, so that battles can be reviewed with animations, sound, etc.
- Write small client libraries for popular languages that parse the JSON into classes, handle creature memory, etc.
- **Realtime** gameplay: make a hybrid version of the game where control is shared by the AI and the player (e.g.: through an action command REPL).
