import sys
import json
from random import random

def think(info):
    response = {"memory": info["memory"]}

    response["action"] = "move"
    response["dx"] = int((3)*random()) - 1
    response["dy"] = int((3)*random()) - 1

    return response

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        info = json.load(f)

    response = think(info)

    with open(sys.argv[2], 'w') as f:
        json.dump(response, f)

    sys.exit(0)
    