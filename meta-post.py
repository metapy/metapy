from metapy import Facebook
from metapy import Twitter

services = [Facebook.FacebookPostService(), Twitter.TwitterPostService()]
for s in services:
	s.post("[[<<< POSTING FROM METAPY >>>]]")
