from __future__ import absolute_import
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
	serviceName = "Facebook"
	def __init__(self, friend):
		self.name = friend["name"]
		self.id = friend["id"]
		
	def serviceLink(self):
		return 'http://www.facebook.com/profile.php?id='+self.id
		
	def serviceId(self):
		return self.id

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
		self.service_id = post["id"]

def get_latest_posts():
	#[TODO] paging vs just 'data' object
	return [FacebookPost(post) for post in api.get_connections("me", "feed")['data']]
	
def submit_post(msg):
	api.put_wall_post(msg)

#
# photos
#

class FacebookPhoto(metapy.Photo):
	def __init__(self, photo):
		self.source = photo['source']
		self.width = photo['width']
		self.height = photo['height']

def get_latest_photos():
	#[TODO] paging vs just 'data' object
	return [FacebookPhoto(photo) for photo in api.get_connections("me", "photos")['data']]
