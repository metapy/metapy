import sys, pickle, getpass
import auth.oauth1

if len(sys.argv) == 1:
	print "Usage: python authorize.py twitter google flickr ..."
	print "Creates an authorization data file for use with APIs."

data = {}

for arg in sys.argv[1:]: 
	print "\n########################################################################"
	
	if arg == "twitter":
		data['twitter'] = {
			'CONSUMER_KEY': "XqEpWilg4foCJzpDhU6aZw",
			'CONSUMER_SECRET': "N9ix9c3nuebmHOoT85W6g04lZBBbRz5qd0iwaOYZY"
		}
		
		OAUTH_SETTINGS = {
		  'auth_params': {},
		  'request_token_url':"http://api.twitter.com/oauth/request_token",
		  'authorize_url':'https://api.twitter.com/oauth/authorize',
		  'access_token_url':'https://api.twitter.com/oauth/access_token',
		}
		oauth_token, oauth_token_secret = auth.oauth1.get_token(OAUTH_SETTINGS,
			data['twitter']['CONSUMER_KEY'], data['twitter']['CONSUMER_SECRET'])
		
		data['twitter']['OAUTH_TOKEN'] = oauth_token
		data['twitter']['OAUTH_TOKEN_SECRET'] = oauth_token_secret
	
		raw_input("Hit enter to continue...")
		
	elif arg == "google":
		data['google'] = {
			'CONSUMER_KEY': "anonymous",
			'CONSUMER_SECRET': "anonymous"
		}

		OAUTH_SETTINGS = {
		  'auth_params': {"scope": ' '.join([
				"https://www.google.com/analytics/feeds/",
				"http://www.google.com/base/feeds/",
				"https://sites.google.com/feeds/",
				"http://www.blogger.com/feeds/",
				"http://www.google.com/books/feeds/",
				"http://www.google.com/calendar/feeds/",
				"http://www.google.com/m8/feeds/",
				"https://docs.google.com/feeds/",
				"http://finance.google.com/finance/feeds/",
				"https://mail.google.com/mail/feed/atom/",
				"http://maps.google.com/maps/feeds/",
				"http://picasaweb.google.com/data/",
				"http://www.google.com/sidewiki/feeds/",
				"https://spreadsheets.google.com/feeds/",
				"http://www.google.com/webmasters/tools/feeds/",
				"http://gdata.youtube.com"])},
		  'request_token_url':"https://www.google.com/accounts/OAuthGetRequestToken",
		  'authorize_url':'https://www.google.com/accounts/OAuthAuthorizeToken',
		  'access_token_url':'https://www.google.com/accounts/OAuthGetAccessToken',
		}
		oauth_token, oauth_token_secret = auth.oauth1.get_token(OAUTH_SETTINGS,
			data['google']['CONSUMER_KEY'], data['google']['CONSUMER_SECRET'])
		
		data['google']['OAUTH_TOKEN'] = oauth_token
		data['google']['OAUTH_TOKEN_SECRET'] = oauth_token_secret
	
		raw_input("Hit enter to continue...")
		
	elif arg == "mailserver":
		data['mailserver'] = {
			"DOMAIN_USERNAME": raw_input("Username@domain.com: "),
			"PASSWORD": getpass.getpass("Password: ")
		}
		
	else:
		print "Unknown service " + arg
	
# write out all auth data
AUTH_FILE = "../auth.p"
pickle.dump(data, open(AUTH_FILE, "wb"))
print "\nAuthorization data saved to " + AUTH_FILE
