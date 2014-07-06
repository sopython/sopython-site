#!/usr/bin/env python3.3
import gzip
import json

def parseResponse (response, decodeJson=True):
	'''Parse the HTTP response, and optionally decode JSON.'''
	content = response.read()
	if response.headers.get('content-encoding') == 'gzip':
		content = gzip.decompress(content)

	if decodeJson:
		try:
			return json.loads(content.decode())
		except ValueError:
			pass

	return content.decode()
