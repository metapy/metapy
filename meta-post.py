from metapy import Facebook
from metapy import Twitter

services = [Facebook.FacebookPostService(), Twitter.TwitterPostService()]

msg = raw_input("Message: ")
for s in services:
	s.post(msg)
