from metapy import Facebook, Twitter, Google

photos = [] + Facebook.get_latest_photos() + Google.get_latest_photos()
for photo in photos:
	print "Photo: %s" % photo.source
