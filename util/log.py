import time

LOGGING = True

def timestamp():
	return time.strftime("%d %b %Y %H:%M:%S", time.gmtime())

def disable():
	LOGGING = False

def enable():
	LOGGING = True

def log(context="GLOBAL", message):
  print "{}\t[{}] - {}".format(timestamp(), context, message)