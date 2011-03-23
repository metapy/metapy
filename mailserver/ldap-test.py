import sys, ldap
from ldap.controls import SimplePagedResultsControl
import pickle

try:
	auth = pickle.load(open("../auth.p"))
	data = auth['mailserver']
except Exception:
	print "ERROR: Run 'authorize.py twitter' first!"
	exit()

if len(sys.argv) == 1:
	print "Usage: python ldap-test.py keyword"
	exit()

Server = "ldap://ldap.olin.edu"
DN = data['DOMAIN_USERNAME']
Secret = data['PASSWORD']
un = sys.argv[1]

#http://www.novell.com/communities/node/1327/sample%20code:%20paging%20searches%20edirectory,%20ldap

Base = "dc=olin,dc=edu"
Scope = ldap.SCOPE_SUBTREE
Filter = "(&(objectClass=user)(givenName=*)(name=*"+un+"*))"
Attrs = ["displayName", "c", "l", "givenName"]

l = ldap.initialize(Server)
l.set_option(ldap.OPT_REFERRALS, 0)
l.protocol_version = 3
print l.simple_bind_s(DN, Secret)

r = l.search_ext(Base, Scope, Filter, Attrs, sizelimit=1000)
Type,user = l.result(r, 100)
for Name,Attrs in user:
	if hasattr(Attrs, 'has_key'):
		if Attrs.has_key('displayName') and Attrs.has_key('givenName'):
			print Attrs['displayName'][0]

sys.exit()
