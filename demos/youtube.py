import gdata.youtube
import gdata.youtube.service

def PrintVideoFeed(feed):
  for entry in feed.entry:
    PrintEntryDetails(entry)

def PrintEntryDetails(entry):
	print 'Video title: %s' % entry.media.title.text
	print 'Video published on: %s ' % entry.published.text
	print 'Video description: %s' % entry.media.description.text
	print 'Video category: %s' % entry.media.category[0].text
	print 'Video tags: %s' % entry.media.keywords.text
	print 'Video watch page: %s' % entry.media.player.url
	print 'Video flash player URL: %s' % entry.GetSwfUrl()
	print 'Video duration: %s' % entry.media.duration.seconds


  # show alternate formats
	for alternate_format in entry.media.content:
		if 'isDefault' not in alternate_format.extension_attributes:
			print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                 alternate_format.url)

  # show thumbnails
 	for thumbnail in entry.media.thumbnail:
		print 'Thumbnail url: %s' % thumbnail.url


def GetAndPrintVideoFeed(uri):
  yt_service = gdata.youtube.service.YouTubeService()
  feed = yt_service.GetYouTubeVideoFeed(uri)
  for entry in feed.entry:
    PrintEntryDetails(entry) # full documentation for this function

yt_service = gdata.youtube.service.YouTubeService()
"""
yt_service.email = ''
yt_service.password = ''
yt_service.source = 'test'
yt_service.ProgrammaticLogin()
"""

entry = yt_service.GetYouTubeVideoEntry(video_id='31CE2BYicyU')
PrintEntryDetails(entry)
print
PrintVideoFeed(yt_service.GetTopFavoritesVideoFeed())


