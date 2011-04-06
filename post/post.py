'''
Created on Mar 23, 2011

@author: gvillenave
'''

import facebookoauth, facebook
import twitter, getpass
import oauth2 as oauth

import pickle

# Test for auth
try:
    auth = pickle.load(open("../auth.p"))
except Exception:
    print "ERROR: Run 'authorize.py' first!"
    exit()
    
# Twitter API
api = twitter.Api(
    consumer_key=data['twitter']['CONSUMER_KEY'],
    consumer_secret=data['twitter']['CONSUMER_SECRET'],
    access_token_key=data['twitter']['OAUTH_TOKEN'],
    access_token_secret=data['twitter']['OAUTH_TOKEN_SECRET']
    )

# Ask for user input
status = raw_input('Enter your message')

# Post status to Twitter
status = api.PostUpdate(status)
print status.text

# Post status to Facebook
graph = facebook.GraphAPI(data["facebook"]["ACCESS_TOKEN"])
graph.put_wall_post(status)
