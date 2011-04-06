import twitter, pickle, metapy

try:
	auth = pickle.load(open("auth.p"))
	data = auth['twitter']
except Exception:
	print "ERROR: Run 'authorize.py twitter' first!"
	exit()

# API stuff
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
	def __init__(self, user):
		self.name = user.name

#
# post service
#

class TwitterPostService(metapy.PostService):
	def post(self, msg):
		api.PostUpdate(msg)

# 
# contacts
#

def get_contacts():
	friends = api.GetFriends()
	return [TwitterPerson(u) for u in friends]
