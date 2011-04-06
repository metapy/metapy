import imaplib, smtplib, email
import email.utils
from email.utils import getaddresses
from email.mime.text import MIMEText

import getpass, pprint, re

# http://www.doughellmann.com/PyMOTW/imaplib/

VERBOSE = True

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

if __name__ == '__main__':
	HOSTNAME = "imaps.olin.edu"
	USERNAME = raw_input("Username: ")
	PASSWORD = getpass.getpass()

	i = IMAPConnection(HOSTNAME)
	i.authenticate(USERNAME, PASSWORD)
	try:
		boxes = i.list_mailboxes()
		print i.get_inbox().get_messages()[0].get_email()
	finally:
		i.close()
	
	s = SMTPConnection('smtps.olin.edu')
	s.authenticate(USERNAME, PASSWORD)

	msg = MIMEText('We should find someone immediately and ask them.')
	msg['To'] = email.utils.formataddr(('Tim Ryan', 'timothy.ryan@students.olin.edu'))
	msg['From'] = email.utils.formataddr(('Timothy Ryan', 'timothy.ryan@students.olin.edu'))
	msg['Subject'] = 'Weekend plans?'
	#s.send_email(msg)
