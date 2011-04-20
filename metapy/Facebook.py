import facebook, metapy, pickle

try:
	auth = pickle.load(open("auth.p"))
	data = auth['facebook']
except Exception:
	print "ERROR: Run 'authorize.py facebook' first!"
	exit()

# API
api = facebook.GraphAPI(data["ACCESS_TOKEN"])

#
# person
#

class FacebookPerson(metapy.Person):
	def __init__(self, name, idNum):
		self.name = name
		self.idNum = idNum

#
# post
#

class FacebookPostService(metapy.PostService):
	def post(self, msg):
		graph = get_facebook_graph()
		graph.put_wall_post(msg)

#
# contacts
#

def get_contacts():
	processedFriends = []
	user = api.get_object("me")
	friends = api.get_connections(user["id"], "friends")
	return [FacebookPerson(friend["name"], friend["id"]) for friend in friends["data"]]
