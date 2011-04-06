import facebook, pickle, metapy


class FacebookPerson():
	def __init__(self, name, idNum):
		self.name = name
		self.idNum = idNum

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
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	user = graph.get_object("me")
	friends = graph.get_connections(user["id"], "friends")
	for friend in friends["data"]:
		f = FacebookPerson(friend["name"], friend["id"]);
		processedFriends.append(f)
	return processedFriends		

def get_contacts():
	return createFacebookFriends(getFacebookAcessToken())
