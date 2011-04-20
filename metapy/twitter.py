from __future__ import absolute_import
import twitter, metapy, pickle, re

try:
	auth = pickle.load(open("auth.p"))
	data = auth['twitter']
except Exception:
	print "ERROR: Run 'authorize.py twitter' first!"
	exit()

# API
api = twitter.Api(
	consumer_key=data['CONSUMER_KEY'],
	consumer_secret=data['CONSUMER_SECRET'],
	access_token_key=data['OAUTH_TOKEN'],
	access_token_secret=data['OAUTH_TOKEN_SECRET']
	)

#
# person
#

class TwitterPerson(metapy.Person):
	serviceName = 'Twitter'
	def __init__(self, user):
		self.twitterHandle = user.screen_name
		self.twitterLink = user.url
		self.name = user.name or ""
		self.given_name = re.search(r'^\S+|^', self.name).group(0)
		self.surname = re.search(r'\S+$|$', self.name).group(0)
	
	def serviceId(self):
		return self.twitterHandle
		
	def serviceLink(self):
		return self.twitterLink
		

def get_contacts():
	friends = api.GetFriends()
	return [TwitterPerson(u) for u in friends]

#
# post
#

class TwitterPost(metapy.Post):
	def __init__(self, post):
		self.message = post.text
		self.time = post.created_at
		self.service_id = post.id

def get_latest_posts():
	#[TODO] paging vs just 'data' object
	return [TwitterPost(post) for post in api.GetFriendsTimeline()]

def submit_post(msg):
	api.PostUpdate(msg)
