#!/usr/bin/env python3.3
from flask import Flask, abort, redirect, render_template, request, session, url_for
from types import SimpleNamespace
import pymongo
import sanction
import urllib.error, urllib.parse

from utils import parseResponse
from filters import registerFilters
from functools import reduce
from allowed import ALLOWED

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import markdown

app = Flask(__name__)
app.config.from_envvar('SOPYTHON_SETTINGS')

registerFilters(app)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

# auth
oauthConfig = SimpleNamespace(id=app.config['OAUTH2_ID'], 
			      secret=app.config['OAUTH2_SECRET'], 
			      key=app.config['OAUTH2_KEY')
oauthClient = sanction.Client(
	auth_endpoint='https://stackexchange.com/oauth',
	token_endpoint='https://stackexchange.com/oauth/access_token',
	resource_endpoint='https://api.stackexchange.com/2.0',
	client_id=oauthConfig.id,
	client_secret=oauthConfig.secret)

# database
db = pymongo.MongoClient()

# views
@app.route('/')
def cabbage ():
	return render_template('index.html')

@app.route('/etiquette')
@app.route('/chatroom')
def etiquette ():
	return render_template('etiquette.html')

@app.route('/salad')
def salad ():
	return render_template('salad.html')

@app.route('/questions')
def questions():
	return redirect(url_for('wiki_view', path='common-questions'))

@app.route('/questions-old')
def questions_old ():
	title = 'Common questions'

	group = {
		"name": "ungrouped",
		"title": "Ungrouped questions",
		"questions": list(db.sopython.questions.find())
	}

	return render_template('questions.html', title=title, groups=[group])

@app.route('/timeline/<qid>/')
def timeline (qid):
	post = db.stackoverflow.posts.find_one({ '_id': qid })
	if not post:
		abort(404)

	return render_template('timeline.html', post=post)


# Authorization
@app.route('/authorize')
def authorize ():
	redirectUri = url_for('authorize', redirect=request.args.get('redirect'), _external=True)
	try:
		oauthClient.request_token(redirect_uri=redirectUri, code=request.args['code'],
			parser=lambda data: dict(urllib.parse.parse_qsl(data)))
	except urllib.error.URLError as e:
		return parseResponse(e, decodeJson=False), 500

	try:
		data = { 'site': 'stackoverflow.com', 'key': oauthConfig.key }
		resp = parseResponse(oauthClient.request('/me?{}'.format(urllib.parse.urlencode(data)), raw=True))
	except urllib.error.URLError as e:
		return parseResponse(e, decodeJson=False), 500

	# set session data
	session['access_token'] = oauthClient.access_token
	session['user'] = resp['items'][0]

	return redirect(request.args.get('redirect', url_for('cabbage')))

@app.route('/login')
def login ():
	redirectUri = url_for('authorize', redirect=request.args.get('redirect'), _external=True)
	return redirect(oauthClient.auth_uri(redirect_uri=redirectUri))

@app.route('/logout')
def logout ():
	# clear session data
	session['access_token'] = None
	session['user'] = None

	return redirect(request.args.get('redirect', url_for('cabbage')))

@app.route('/wiki/')
def wiki_main():
	tree = cache.get('wiki-toc')
	if tree is None:
		tree = generate_wiki_toc()
		cache.set('wiki-toc', tree, 900)
	return render_template('wiki-main.html', toc=tree, pages=db.sopython.wiki.find({}, ['_id', 'title']))

@app.route('/wiki/<path:path>', methods=['GET'])
def wiki_view(path):
	entry = db.sopython.wiki.find_one({'_id': path})
	if not entry and session.get('user', {}).get('user_id') not in ALLOWED:
		abort(404)
	if not entry:
		return render_template('wiki-edit.html', path=path)
	if session.get('user', {}).get('user_id') in ALLOWED:
		if 'delete' in request.args:
			db.sopython.wiki.remove(entry['_id'])
			return redirect(url_for('cabbage'))
		if 'edit' in request.args:
			return render_template('wiki-edit.html', path=path, **entry)
	return render_template(
		'wiki-entry.html',
		title = entry['title'],
		body = markdown.markdown(entry['body'], extensions=['codehilite(linenums=False)']),
		name = entry['user']['display_name'],
		image = entry['user']['profile_image'],
		path = path
	)

@app.route('/wiki/<path:path>', methods=['POST'])
def wiki_post(path):
	if session.get('user', {}).get('user_id') not in ALLOWED:
		abort(401)
	db.sopython.wiki.save({
		'_id': path,
		'title': request.form['title'],
		'body': request.form['body'],
		'user': session['user']
	})
	return redirect(url_for('wiki_view', path=path))

def generate_wiki_toc():
	#tree = {}
	#for item in db.sopython.wiki.find({}, ['_id', 'title']):
        #	path = item['_id'].split('/')
	#        leaf = reduce(lambda a,b:a.setdefault(b, {}), path[:-1], tree)
        #	leaf[path[-1]] = item['title']
	#return tree
	return {}

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8080)
