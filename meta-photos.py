from metapy import facebook, twitter, google

photos = [] + facebook.get_latest_photos() + google.get_latest_photos()
for photo in photos:
	print "Photo: %s" % photo.source
