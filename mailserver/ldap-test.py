import sys, ldap, re, time
from ldap.controls import SimplePagedResultsControl
import pickle

# http://www.novell.com/communities/node/1327/sample%20code%3A%20paging%20searches%20edirectory,%20ldap

page_size = 10

try:
	auth = pickle.load(open("../auth.p"))
	data = auth['mailserver']
except Exception:
	print "ERROR: Run 'authorize.py twitter' first!"
	exit()

class SimpleLDAP:
	def __init__(self, server, base):
		self.server = server
		self.base = base
	
	def authorize(self, dn, secret):
		self.dn = dn
		self.secret = secret
		
		# authorize server
		ldap.set_option(ldap.OPT_REFERRALS, 0)
		self.l = ldap.initialize(self.server)
		self.l.protocol_version = 3
		self.l.simple_bind_s(self.dn, self.secret)
	
	def find_users_by_name(self, keyword):
		keyword = re.sub('[^a-z\s]+', '', keyword)
		ldap_filter = "(&(objectClass=user)(givenName=*)(name=*"+keyword+"*))"
		attrs = ["displayName", "givenName", "sn",
				"company", "mail",
				"streetAddress", "l", "st", "co"]

		lc = SimplePagedResultsControl(
		  ldap.LDAP_CONTROL_PAGE_OID, True, (page_size,'')
		)

		scope = ldap.SCOPE_SUBTREE
		msgid = self.l.search_ext(self.base, scope, ldap_filter, attrs, serverctrls=[lc])
		
		persons = []

		pages = 0
		while True:
			pages += 1
			#print "Getting page %d" % (pages,)
			
			# successive tries sometimes result in unavailable messages
			tries = 5
			try:
				rtype, rdata, rmsgid, serverctrls = self.l.result3(msgid)
			except ldap.UNAVAILABLE_CRITICAL_EXTENSION, e:
				print "LDAP Error: " + str(e)
				return persons
				
			#print '%d results' % len(rdata)
			for search, attrs in rdata:
				try:
					if attrs.has_key('givenName') and attrs.has_key('displayName'):
						persons.append({
							"name": attrs.get('displayName', [''])[0],
							"given_name": attrs.get('givenName', [''])[0],
							"surname": attrs.get('sn', [''])[0],
							"street": attrs.get('streetAddress', [''])[0],
							"city": attrs.get('l', [''])[0],
							"state": attrs.get('st', [''])[0],
							"country": attrs.get('co', [''])[0],
							"company": attrs.get('company', [''])[0],
							"email": attrs.get('mail', [''])[0]
							})
				except AttributeError, e:
					print "Error: %s, skipping..." % str(e)
					
			pctrls = [
				c
				for c in serverctrls
				if c.controlType == ldap.LDAP_CONTROL_PAGE_OID
			]
			
			if pctrls:
				est, cookie = pctrls[0].controlValue
				if cookie:
					lc.controlValue = (page_size, cookie)
					msgid = self.l.search_ext(self.base, scope, ldap_filter,
										 serverctrls=[lc])
				else:
					break
			else:
				print "Warning:  Server ignores RFC 2696 control."
				break
		return persons

if len(sys.argv) == 1:
	print "Usage: python ldap-test.py keyword"
	exit()

server = "ldap://ldap.olin.edu"
base = "dc=olin,dc=edu"

dn = data['DOMAIN_USERNAME']
secret = data['PASSWORD']

keyword = sys.argv[1]
		
s = SimpleLDAP(server, base)
s.authorize(dn, secret)
print s.find_users(keyword)

sys.exit()
