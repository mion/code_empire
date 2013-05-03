import time

LOGGING = True

def timestamp():
	return time.strftime("%d %b %Y %H:%M:%S", time.gmtime())

def disable():
	LOGGING = False

def enable():
	LOGGING = True

def log(message, context="GLOBAL"):
  print "[{}]\t{} - {}".format(timestamp(), context, message)


class BattleLogger(object):
    """BattleLogger writes a log such that a battle can be recreated."""
    def __init__(self, battle_id):
        self.battle_id = battle_id
