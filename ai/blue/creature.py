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
        self.target = info["creatures"].get(self.memory.get("target_id", None), None)
        self.myself = info["myself"]
        self.response = {"memory": self.memory}

    def is_target_insight(self):
        return self.target["id"] in info["creatures"]

    def is_target_in_attack_range(self):
        # TODO: hardcoded attack range
        return Point(self.target["x"], self.target["y"]).distance_to(Point(self.myself["x"], self.myself["y"])) <= 1

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

    def think(self):
        if self.target:
            if self.is_target_insight():
                if self.is_target_in_attack_range():
                    self.attack_target()
                else:
                    self.follow_target()
            else:
                self.lose_target()    
        else:
            self.response["action"] = "wander"

        return self.response


if __name__ == '__main__':
    info_json = sys.argv[1]
    info = json.loads(info_json)

    ai = CreatureAI(info)
    response = ai.think()

    print json.dumps(response)
    sys.exit(0)