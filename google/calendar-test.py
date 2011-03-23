#!/usr/bin/python2

import gdata.calendar.service
import pickle

try:
	auth = pickle.load(open("../auth.p"))
	data = auth['google']
except Exception:
	print "ERROR: Run 'authorize.py google' first!"
	exit()

# API stuff
OAUTH_SCOPES = "http://www.google.com/calendar/feeds/"

# gdata calendar (as of 2.0.13) doesn't yet have a .client, using GDClient
# instead .service uses GDataService(!), hence the grossly different code
client = gdata.calendar.service.CalendarService(source='test-test-v0')
client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, \
	data['CONSUMER_KEY'], consumer_secret=data['CONSUMER_SECRET'])
oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, \
	data['CONSUMER_KEY'], consumer_secret=data['CONSUMER_SECRET']) 
client.SetOAuthToken(gdata.auth.OAuthToken(key=data['OAUTH_TOKEN'], secret=data['OAUTH_TOKEN_SECRET'], \
	scopes=OAUTH_SCOPES, oauth_input_params=oauth_input_params))

feed = client.GetCalendarEventFeed()
print 'Events on Primary Calendar: %s' % (feed.title.text,)
for i, an_event in enumerate(feed.entry):
	print '\t%s. %s' % (i, an_event.title.text,)
	for p, a_participant in enumerate(an_event.who):
		print '\t\t%s. %s' % (p, a_participant.email,)
		print '\t\t\t%s' % (a_participant.name,)
		#print '\t\t\t%s' % (a_participant.attendee_status.value,)
