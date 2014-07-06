#!/usr/bin/env python3.3
import hoedown
import markupsafe
import re

def date (datetime):
	'''Format the datetime.'''
	return datetime.strftime('%Y-%m-%d %H:%M:%S')

def md (text):
	'''Convert the markdown text to HTML.'''
	if not text:
		return text
	return markupsafe.Markup(hoedown.html(text).strip())

def mdi (text):
	'''Convert the inline markdown text to HTML.'''
	if not text:
		return text
	text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
	text = re.sub('\*\*([^`]+)\*\*', '<strong>\\1</strong>', text)
	text = re.sub('\*([^`]+)\*', '<em>\\1</em>', text)
	text = re.sub('`([^`]+)`', '<code>\\1</code>', text)
	return markupsafe.Markup(text.strip())


def registerFilters (app):
	'''Register all jinja filters.'''
	app.add_template_filter(date)
	app.add_template_filter(md)
	app.add_template_filter(mdi)
