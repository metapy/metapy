import sys, pickle, getpass
import auth.oauth1, auth.oauth2

services = []
AUTH_FILE = "../auth.p"

if len(sys.argv) == 1:
	services = ["twitter", "google", "mailserver", "facebook"]
else:
	services = sys.argv[1:]
	
data = {}

for arg in services: 
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
		
		raw_input("Hit enter to continue...")
		
	elif arg == "facebook":
		data['facebook'] = {
			'CONSUMER_KEY': "107434656002093",
			'CONSUMER_SECRET': "4e0836947597ae34b9c13a6363909a05"
		}
		
		OAUTH_SETTINGS = {
		  'auth_params': {"scope": "user_about_me user_activities user_birthday user_education_history user_events user_groups user_hometown user_interests user_likes user_location user_notes user_online_presence user_photo_video_tags user_photos user_relationships user_relationship_details user_religion_politics user_status user_videos user_website user_work_history email read_friendlists read_insights read_mailbox read_requests read_stream xmpp_login ads_management user_checkins publish_stream create_event rsvp_event sms offline_access publish_checkins manage_pages friends_about_me friends_activities friends_birthday friends_education_history friends_events friends_groups friends_hometown friends_interests friends_likes friends_location friends_notes friends_online_presence friends_photo_video_tags friends_photos friends_relationships friends_relationship_details friends_religion_politics friends_status friends_videos friends_website friends_work_history email manage_friendlists friends_checkins"},
		  'endpoint': "graph.facebook.com"
		}
		data["facebook"]["ACCESS_TOKEN"] = auth.oauth2.get_token(OAUTH_SETTINGS,
			data['facebook']['CONSUMER_KEY'], data['facebook']['CONSUMER_SECRET'])
	
		raw_input("Hit enter to continue...")
		
	else:
		print "Unknown service " + arg
	
# write out all auth data
pickle.dump(data, open(AUTH_FILE, "wb"))
print "\nAuthorization data saved to " + AUTH_FILE

print "#################### You are all authorized! ###################"
