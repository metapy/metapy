import sys, os
sys.path.insert(0, os.path.abspath('lib'))
from metapy import Twitter

class Person(object):
	pass
	
class FacebookPerson(Person):
	pass
	
class GTalkPerson(Person):
	pass
	
class MetaMerge(object):
	def __init__(self, cls, facets):
		self.cls = cls
		self.facets = facets
		
	def get(self, prop):
		l = []
		for facet in self.facets:
			if hasattr(facet, prop):
				l.append((getattr(facet, prop), facet))
		return l
		
	def addfacet(self, facet):
		self.facets.append(facet)
	
	def __getattr__(self, prop):
		return self.get(prop)

class ContactBook(object):
	def __init__(self):
		self.contacts = []
		self.contacts_by_name = {}
		self.contacts_by_email = {}
		
	def insert(self, contactfacet):
		email = name = c = None
		if hasattr(contactfacet, 'email'):
			email = contactfacet.email
			c = self.contacts_by_email.get(email, None)
		if hasattr(contactfacet, 'name'):
			name = contactfacet.name.lower()
			c = self.contacts_by_name.get(name, None)
		
		if c:
			c.addfacet(contactfacet)
		else:
			c = MetaMerge(Person, [contactfacet])
			self.contacts.append(c)
			
		if email:
			self.contacts_by_email[email] = c
		if name:
			self.contacts_by_name[name] = c
		

#t = TwitterPerson()
#t.email = 'km@example.com'
#t.name = 'Kevin Mehall'
#t.twitterHandle = '@kevinmehall'

f = FacebookPerson()
f.name = 'Kevin Mehall'
f.phone = '111-222-3333'

g = GTalkPerson()
g.email = 'km@example.com'

g2 = GTalkPerson()
g2.email = 'test@example.com'
g2.name = 'Test person'

c = ContactBook()
c.insert(f)
c.insert(g)
c.insert(g2)

for t in Twitter.get_contacts():
	c.insert(t)

print c.contacts_by_name
#print c.contacts_by_email['km@example.com']
#print c.contacts_by_email['km@example.com'].phone
