import gdata.contacts.client, metapy, pickle

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
	def __init__(self, entry):
		try:
			self.name = entry.name.full_name.text or entry.name
		except:
			self.name = entry.name or ""

def get_contacts():
	groups = contacts.GetGroups()
	contactsGroup = groups.entry[0]

	q = gdata.contacts.client.ContactsQuery()
	q.group = contactsGroup.id.text
	q.max_results = 1000

	feed = contacts.GetContacts(q=q)
	return [GooglePerson(entry) for entry in feed.entry]
