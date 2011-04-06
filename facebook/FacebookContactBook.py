import pickle
import FacebookPerson

def getFacebookAcessToken() :
	try:
		auth = pickle.load(open("../auth.p"))
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
		try:
			f.email = friend["email"]
		except:
			pass
		try:
			f.gender = friend["gender"]
		except:
			pass
		try:
			f.location = friend["location"]
		except:
			pass
		processedFriends.append(f)
		print f.name + f.idNum
	return processedFriends		

def getFacebookContacts():
	return createFacebookFriends(getFacebookAcessToken())
