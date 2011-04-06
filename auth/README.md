# Authorization Script

Generates our pickle'd authorization data for each API.

First you need oauth2:

	git clone https://github.com/simplegeo/python-oauth2.git
	cp -r python-oauth2/oauth2 ./oauth
	rm -rf python-oauth2

Run the <code>authorize.py</code> script with arguments for each API you want to generate data for:

	python authorize.py twitter google flickr ...

This generates auth-*.p files. Copy them to the corresponding directories.
