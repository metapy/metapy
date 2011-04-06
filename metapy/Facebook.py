import facebook, pickle, metapy

# and code
		
def get_facebook_graph():
	return facebook.GraphAPI(getFacebookAcessToken())

def getFacebookAcessToken() :
	try:
		auth = pickle.load(open("auth.p"))
		data = auth['facebook']
	except Exception:
		print "ERROR: Run 'authorize.py facebook' first!"
		exit()
	return data["ACCESS_TOKEN"]
	
def createFacebookFriends(ACCESS_TOKEN):
	processedFriends = []
	graph = get_facebook_graph()
	user = graph.get_object("me")
	friends = graph.get_connections(user["id"], "friends")
	for friend in friends["data"]:
		f = FacebookPerson(friend["name"], friend["id"]);
		processedFriends.append(f)
	return processedFriends		

def get_contacts():
	return createFacebookFriends(getFacebookAcessToken())

# person

class FacebookPerson():
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
