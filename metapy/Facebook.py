import facebook, metapy, pickle, pprint

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
	def __init__(self, friend):
		self.name = friend["name"]
		self.id = friend["id"]

def get_contacts():
	user = api.get_object("me")
	friends = api.get_connections(user["id"], "friends")
	return [FacebookPerson(friend) for friend in friends["data"]]

#
# post
#

class FacebookPost(metapy.Post):
	def __init__(self, post):
		self.message = post["message"] if hasattr(post, "message") else ""
		self.time = post["created_time"]

def get_latest_posts():
	#[TODO] paging vs just 'data' object
	return [FacebookPost(post) for post in api.get_connections("me", "feed")['data']]
	
def submit_post(post):
	api.put_wall_post(post.msg)
