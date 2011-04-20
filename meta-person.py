import sys, os
from metapy import twitter, facebook, google, mailserver
from metapy import Person

class MetaMerge(object):
	def __init__(self, cls, facets):
		self.cls = cls
		self.facets = facets
		
	def get(self, prop):
		l = []
		for facet in self.facets:
			if hasattr(facet, prop):
				vals = getattr(facet, prop)
				if not isinstance(vals, list):
					vals = [vals]
				for v in vals:
					l.append((v, facet))
		return l
		
	def addfacet(self, facet):
		self.facets.append(facet)
	
	def __getattr__(self, prop):
		return self.get(prop)

class ContactBook(object):
	def __init__(self):
		self.contacts = []
		self.contacts_by_name = {}
		
	def insert(self, contactfacet):
		name = c = None
		
		if hasattr(contactfacet, 'name'):
			name = contactfacet.name.lower()
			c = self.contacts_by_name.get(name, None)
		
		# add person
		if c:
			c.addfacet(contactfacet)
		else:
			c = MetaMerge(Person, [contactfacet])
			self.contacts.append(c)
		
		if name:
			self.contacts_by_name[name] = c

c = ContactBook()

for g in google.get_contacts():
	c.insert(g)

for f in facebook.get_contacts():
	c.insert(f)

for t in twitter.get_contacts():
	c.insert(t)

for t in mailserver.get_contacts():
	c.insert(t)

for person in c.contacts_by_name.itervalues():
	nameSources = person.get('name')
	if len(nameSources) > 3:
		print nameSources[0][0]
		for name, source in nameSources:
			print '\t%s: %s'%(source.serviceName, source.serviceId())
