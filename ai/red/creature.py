import sys
import json

def think(info):
    response = {}

    response["action"] = "move"
    response["dx"] = 1
    response["dy"] = 1

    return response

if __name__ == '__main__':
    info_json = sys.argv[1]
    info = json.loads(info_json)

    response = think(info)
    print json.dumps(response)

    sys.exit(0)