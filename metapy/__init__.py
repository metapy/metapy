# add all services to system path
import sys
sys.path.insert(0, "twitter")
sys.path.insert(0, "facebook")
sys.path.insert(0, "google")
sys.path.insert(0, "mailserver")

# person

class Person(object):
	pass

# post service

class PostService(object):
	def post(self, msg):
		pass
