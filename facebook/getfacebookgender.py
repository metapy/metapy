import os, sys
import facebookoauth
import facebook
import json

ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token'
friend_dict = {}
if __name__ == '__main__':
	if len(sys.argv) == 3:
                name = sys.argv[1] + " " + sys.argv[2]
	elif len(sys.argv) == 4:
		name = sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3]
	else:
		print("Usage: getfacebookfriends.py <Name>")
	
	ACCESS_TOKEN = open(LOCAL_FILE).read()
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	user = graph.get_object("me")
	friends = graph.get_connections(user["id"], "friends")
	for friend in friends["data"]:
		friend_dict[friend["name"]] = friend["id"]
	frid = friend_dict[name]
	fr = graph.get_object(frid)
	print  name + " is a " + fr["gender"]
    


