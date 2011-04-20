import sys, ldap, re, time, metapy
from ldap.controls import SimplePagedResultsControl
import imaplib, smtplib, email
import email.utils
from email.utils import getaddresses
from email.mime.text import MIMEText

import re, pickle

try:
	auth = pickle.load(open("auth.p"))
	data = auth['mailserver']
except Exception:
	print "ERROR: Run 'authorize.py mailserver' first!"
	exit()
	
#
# custom API
#

VERBOSE = True
PAGE_SIZE = 10

# http://www.novell.com/communities/node/1327/sample%20code%3A%20paging%20searches%20edirectory,%20ldap

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
		  ldap.LDAP_CONTROL_PAGE_OID, True, (PAGE_SIZE,'')
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
					lc.controlValue = (PAGE_SIZE, cookie)
					msgid = self.l.search_ext(self.base, scope, ldap_filter,
										 serverctrls=[lc])
				else:
					break
			else:
				print "Warning:  Server ignores RFC 2696 control."
				break
		return persons

# http://www.doughellmann.com/PyMOTW/imaplib/

class IMAPConnection:
	def __init__(self, hostname):
		self.hostname = hostname
		if VERBOSE: print '[IMAP] Connecting to', hostname
		self.conn = imaplib.IMAP4_SSL(hostname)

	def authenticate(self, username, password):
		if VERBOSE: print '[IMAP] Logging in as', username
		self.conn.login(username, password)
		
	def get_mailbox(self, name):
		return IMAPMailbox(self.conn, name, '\\', '')
		
	def get_inbox(self):
		return self.get_mailbox('INBOX')

	# kargs: directory="Trash", pattern="*ras*"
	def list_mailboxes(self, **kargs):
		list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
		boxes = []
		typ, data = self.conn.list(**kargs)
		if typ == "OK":
			for box in data:
				flags, delimiter, mailbox_name = list_response_pattern.match(box).groups()
				mailbox_name = mailbox_name.strip('"')
				boxes.append(IMAPMailbox(self.conn, mailbox_name, delimiter, flags))
		return boxes
		
	def close(self):
		self.conn.logout()

class IMAPMailbox:
	def __init__(self, conn, name, delimiter, flags):
		self.conn = conn
		self.name = name
		self.delimiter = delimiter
		self.levels = name.split(delimiter)
		self.flags = flags # imaplib.ParseFlags
	
	# UIDNEXT, UIDVALIDITY, MESSAGES, UNSEENS, RECENT
	def get_status(self):
		stat_pattern = re.compile(r'(?P<mailbox>.*) \((?P<status>.*)\)')
		typ, stat = self.conn.status(self.name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)')
		mailbox, data = stat_pattern.match(stat[0] or '').groups()
		data = re.split(r'\s+', data)
		return dict(zip(data[::2], data[1::2]))
	
	def unread_count(self):
		typ, data = self.conn.select(self.name)
		if typ == 'OK':
			return int(data[0])
		return None
		
	def get_messages(self):
		return self.search_messages('ALL')
		
	def search_messages(self, criteria=None):
		self.conn.select(self.name)
		typ, ids = self.conn.search(None, criteria)
		if typ != 'OK':
			return []
		ids = re.split(r'\s+', ' '.join(ids))
		messages = []
		for id in ids:
			messages.append(IMAPMessage(self.conn, self, id))
		return messages
	
	def add_email(self, new_message, mailbox='INBOX'):
		self.conn.append(mailbox,
			'',	imaplib.Time2Internaldate(time.time()), str(new_message))

class IMAPMessage:
	def __init__(self, conn, mailbox, id):
		self.conn = conn
		self.mailbox = mailbox
		self.id = str(id)
	
	def get_flags(self):
		self.conn.select(self.mailbox.name)
		typ, msg_data = self.conn.fetch('1', '(FLAGS)')
		for response_part in msg_data:
			return imaplib.ParseFlags(response_part)
		return ''
	
	def get_email(self):
		self.conn.select(self.mailbox.name)
		typ, msg_data = self.conn.fetch('1', '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				return email.message_from_string(response_part[1])
		return None

class SMTPConnection:
	def __init__(self, hostname):
		self.hostname = hostname
		self.conn = smtplib.SMTP(hostname)
		self.conn.ehlo()

		# If we can encrypt this session, do it
		# re-identify ourselves over TLS connection
		if self.conn.has_extn('STARTTLS'):
			self.conn.starttls()
			self.conn.ehlo()

	def authenticate(self, username, password):
		self.conn.login(username, password)
		
	def send_email(self, msg):
		froma = msg.get_all('from', '')
		tos = msg.get_all('to', [])
		ccs = msg.get_all('cc', [])
		resent_tos = msg.get_all('resent-to', [])
		resent_ccs = msg.get_all('resent-cc', [])
		all_recipients = tos + ccs + resent_tos + resent_ccs
		self.conn.sendmail(' '.join(froma), ' '.join(all_recipients), msg.as_string())
			
	def close(self):
		self.conn.quit()

#
# person
#

server = "ldap://ldap.olin.edu"
base = "dc=olin,dc=edu"
		
s_ldap = SimpleLDAP(server, base)
s_ldap.authorize(data['DOMAIN_USERNAME'], data['PASSWORD'])

class MailserverPerson(metapy.Person):
	serviceName = 'Mailserver'
	
	def __init__(self, user):
		self.email = user['email']
		self.name = user['name']
		
	def serviceId(self):
		return self.email
		
	def serviceLink(self):
		return None
		
def get_contacts():
	return [MailserverPerson(u) for u in s_ldap.find_users_by_name("a")]
