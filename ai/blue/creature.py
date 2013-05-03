import sys
import json


class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "({}, {})".format(self.x, self.y)

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

class CreatureAI(object):
    def __init__(self, info):
        self.info = info
        self.memory = info["memory"]
        self.myself = info["myself"]
        self.response = {"memory": self.memory, 'log': []}
        self.target = self.get_target() #info["creatures"].get(self.memory.get("target_id", None), None)
        self.log("Starting round... memory: {}".format(self.memory))
        self.log("Target: {}".format(self.get_target()))
        self.log("Creatures: {}".format(self.info["creatures"]))

    def is_target_insight(self):
        return self.target["id"] in info["creatures"]

    def is_target_in_attack_range(self):
        # TODO: hardcoded attack range
        return Point(self.target["x"], self.target["y"]).distance_to(Point(self.myself["x"], self.myself["y"])) <= 1

    def get_target(self):
        return self.info["creatures"].get(self.memory.get("target_id", None), None)

    def lose_target(self):
        del self.memory["target_id"]

    def target_dx_dy(self):
        return Point(self.myself["x"], self.myself["y"]).dx_dy(Point(self.target["x"], self.target["y"])) 

    def attack_target(self):
        self.response["action"] = "attack"
        self.response["target_x"] = self.target["x"]
        self.response["target_y"] = self.target["y"]

    def follow_target(self):
        self.response["action"] = "move"
        self.response["dx"], self.response["dy"] = self.target_dx_dy()

    def find_target(self):
        for cid in self.info["creatures"]:
            creature = self.info["creatures"][cid]
            if creature["player"] != self.myself["player"]:
                self.memory["target_id"] = creature["id"]
                self.target = creature
                return True

        return False

    def log(self, message):
        with open(self.myself["player"] + '_battle.log', 'a') as f:
            f.write('{} at ({}, {}) -> {}\n'.format(self.myself["name"], self.myself["x"], self.myself["y"], message))
        self.response['log'].append(message)

    def think(self):
        if self.target:
            self.log("I have a target.")
            if self.is_target_insight():
                self.log("Target is insight.")
                if self.is_target_in_attack_range():
                    self.log("Target is close! attacking...")
                    self.attack_target()
                else:
                    self.log("Target is not close, following...")
                    self.follow_target()
            else:
                self.log("Target lost.")
                self.lose_target()
        else:
            self.log("I don't have a target.")
            if self.find_target():
                self.log("Target found: {}. Following...".format(self.target))
                self.follow_target()
            else:
                self.log("No target insight, wandering...")
                self.response["action"] = "wander"

        return self.response


if __name__ == '__main__':
    info_json = sys.argv[1]
    info = json.loads(info_json)

    ai = CreatureAI(info)
    response = ai.think()

    print json.dumps(response)
    sys.exit(0)