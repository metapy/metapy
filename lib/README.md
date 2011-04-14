OAuth2
===========

## Installation

	git clone https://github.com/simplegeo/python-oauth2.git
	mv python-oauth2/oauth2 .
	rm -rf python-oauth2

Twitter
=======

## Installation

	hg clone http://python-twitter.googlecode.com/hg/ python-twitter
	mv python-twitter/twitter.py .
	rm -rf python-twitter

Facebook
========

## Installation

	git clone https://github.com/facebook/python-sdk.git
	mv python-sdk/src/facebook.py .
	rm -rf python-sdk

Google Data
===========

## Installation

[GData API reference](http://code.google.com/p/gdata-python-client/)

	easy_install gdata # current version

or

	sudo apt-get install python-gdata # slightly earlier version

## Reference

 * [Contacts API Docs (incomplete, broken, and wrong)](http://code.google.com/apis/contacts/docs/3.0/developers_guide_python.html)
 * [Calendar API Docs](http://code.google.com/apis/calendar/data/1.0/developers_guide_python.html#AuthClientLogin)

Mailserver
==========

Connects with LDAP, IMAP/POP, and SMTP.

## Installation

	sudo apt-get install python-ldap

You can now use ldap with <code>import ldap</code>. <code>imaplib</code>, <code>poplib</code>, and <code>smtplib</code> are all included by default in Python.

