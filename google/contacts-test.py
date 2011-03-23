#!/usr/bin/python2

import gdata.contacts.client
import pickle

try:
	auth = pickle.load(open("../auth.p"))
	data = auth['google']
except Exception:
	print "ERROR: Run 'authorize.py google' first!"
	exit()

client=gdata.contacts.client.ContactsClient(source='test-test-v0')
client.auth_token = gdata.gauth.OAuthHmacToken(data['CONSUMER_KEY'], data['CONSUMER_SECRET'],
	data['OAUTH_TOKEN'], data['OAUTH_TOKEN_SECRET'], gdata.gauth.ACCESS_TOKEN)

groups = client.GetGroups()
contactsGroup = groups.entry[0]

q = gdata.contacts.client.ContactsQuery()
q.group = contactsGroup.id.text
q.max_results = 1000

feed = client.GetContacts(q=q)

for entry in feed.entry:
    try:
        print entry.name.full_name.text
    except:
        print entry.name



