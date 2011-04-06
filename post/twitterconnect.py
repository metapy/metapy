import twitter, getpass
import oauth2 as oauth

import pickle

try:
	auth = pickle.load(open("../auth.p"))
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

print "People who have recently posted statuses:"
statuses = api.GetPublicTimeline()
print [s.user.name for s in statuses]
print ""

print "Your friends:"
friends = api.GetFriends()
print [u.name for u in friends]
