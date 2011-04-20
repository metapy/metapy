from metapy import Facebook, Twitter

#services = [Facebook.FacebookPostService(), Twitter.TwitterPostService()]
#msg = raw_input("Message: ")
#for s in services:
#	s.post(msg)

print Facebook.get_latest_posts()
print Twitter.get_latest_posts()
