from __future__ import absolute_import
import gdata.contacts.client, gdata.photos.service
import metapy, pickle

try:
	auth = pickle.load(open("auth.p"))
	data = auth['google']
except Exception:
	print "ERROR: Run 'authorize.py google' first!"
	exit()

#
# person
#

contacts = gdata.contacts.client.ContactsClient(source='test-test-v0')
contacts.auth_token = gdata.gauth.OAuthHmacToken(data['CONSUMER_KEY'], data['CONSUMER_SECRET'],
	data['OAUTH_TOKEN'], data['OAUTH_TOKEN_SECRET'], gdata.gauth.ACCESS_TOKEN)

class GooglePerson(metapy.Person):
	serviceName = "Google"
	def __init__(self, entry):
		try:
			self.name = entry.name.full_name.text or entry.name
		except:
			self.name = entry.name or ""
			
		self.email = [e.address for e in entry.email]
			
	def serviceLink(self):
		return None
	def serviceId(self):
		return ','.join(self.email)

#
# photos
#			

class GooglePhoto(metapy.Photo):
	def __init__(self, photo):
		#print photo.title.text
		self.source = photo.GetMediaURL()
		self.width = int(photo.width.text)
		self.height = int(photo.height.text)

def get_contacts():
	groups = contacts.GetGroups()
	contactsGroup = groups.entry[0]

	q = gdata.contacts.client.ContactsQuery()
	q.group = contactsGroup.id.text
	q.max_results = 1000

	feed = contacts.GetContacts(q=q)
	return [GooglePerson(entry) for entry in feed.entry]

# 2.0.13 doesn't have a client for photos, using service
OAUTH_SCOPES = "http://picasaweb.google.com/data/"
photos = gdata.photos.service.PhotosService(source='test-test-v0')
photos.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, \
	data['CONSUMER_KEY'], consumer_secret=data['CONSUMER_SECRET'])
oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, \
	data['CONSUMER_KEY'], consumer_secret=data['CONSUMER_SECRET']) 
photos.SetOAuthToken(gdata.auth.OAuthToken(key=data['OAUTH_TOKEN'], secret=data['OAUTH_TOKEN_SECRET'], \
	scopes=OAUTH_SCOPES, oauth_input_params=oauth_input_params))

#http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.photos.service.html#PhotosService
#http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.photos.html#AlbumEntry

def get_latest_photos():
	# get all albums
	feed = photos.GetUserFeed()
	res = []
	for album in feed.entry:
		for photo in photos.GetFeed(album.GetPhotosUri()).entry:
			res.append(GooglePhoto(photo))
	return res
