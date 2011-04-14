Metapy
======

A Python environment for interacting with your web data.

# Authentication Script

Generates our pickle'd authorization data for each API.

Run the <code>authenticate.py</code> script with arguments for each API you want to generate data for:

	python authenticate.py twitter google flickr ...

or for all of them:

	python authenticate.py

This generates a pickled data structure <code>auth.p</code> with your credentials.
