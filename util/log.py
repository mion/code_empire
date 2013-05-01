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