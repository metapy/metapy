from metapy import facebook, twitter

#msg = raw_input("Message: ")
#services = [Facebook.submit_post, Twitter.submit_post]
#for submit_post in services:
#	submit_post(msg)

print facebook.get_latest_posts()
print twitter.get_latest_posts()
