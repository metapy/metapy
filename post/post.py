'''
Created on Mar 23, 2011

@author: gvillenave
'''

import facebookoauth
import twitter, getpass
import oauth2 as oauth

import pickle

try:
    auth = pickle.load(open("../auth.p"))
    data = auth['twitter']
except Exception:
    print "ERROR: Run 'authorize.py twitter' first!"
    exit()
    
# Twitter API
api = twitter.Api(
    consumer_key=data['CONSUMER_KEY'],
    consumer_secret=data['CONSUMER_SECRET'],
    access_token_key=data['OAUTH_TOKEN'],
    access_token_secret=data['OAUTH_TOKEN_SECRET']
    )

# Post status to Twitter
status = api.PostUpdate('{Test tweet from Python API}')
print status.text
