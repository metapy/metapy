from metapy import Facebook, Twitter

#msg = raw_input("Message: ")
#services = [Facebook.submit_post, Twitter.submit_post]
#for submit_post in services:
#	submit_post(msg)

Facebook.get_latest_posts()
Twitter.get_latest_posts()
