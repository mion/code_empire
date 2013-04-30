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
    info_json = sys.argv[1]
    info = json.loads(info_json)

    response = think(info)
    print json.dumps(response)

    sys.exit(0)