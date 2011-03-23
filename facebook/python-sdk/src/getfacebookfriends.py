import os, sys
import facebookoauth
import facebook
import json

ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token'
friend_dict = {}
if __name__ == '__main__':	
	ACCESS_TOKEN = open(LOCAL_FILE).read()
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	user = graph.get_object("me")
	friends = graph.get_connections(user["id"], "friends")
	for friend in friends["data"]:
		print friend["name"] + ":" + friend["id"]


