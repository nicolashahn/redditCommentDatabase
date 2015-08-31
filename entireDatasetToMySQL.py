# NLDS Lab
# Nicolas Hahn
# A script to take raw Reddit JSON data 
# and insert it to a MySQL DB based on IAC schema
# input: Raw Reddit JSON post objects in text format, one object per line
# output: MySQL insertions for each object according to schema
# the 1 month dataset has 53,851,542 comments total

# -*- coding: utf-8 -*-

import json
import sqlalchemy as s
import oursql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.dialects import mysql
import sys
import re
# import markdown2 as md
# import mistune
import snudown
import datetime

###################################
# Global variables
###################################

# because 1-5 appear to be taken in IAC
reddit_id = 6

# how many objects to push to server at a time
batch_size = 1000

# reuse parser for faster results
markdown = snudown.markdown

# {native_id: db_id}
# so we don't have to query to check if link/subreddit obj already exists
link_dict = {}
subreddit_dict = {}
author_dict = {}
post_dict = {}

# temporary output file for checking things 
# (print statements choke on unicode)
tempOut = open('tempOut','w', encoding='utf-8')


###################################
# JSON data manipulation
###################################

# json text dump -> list of json-dicts
# also encodes the line number the object in the raw file
def jsonLineToDict(line):
	jObj = json.loads(line)
	jObj = removeNonUnicode(jObj)
	return jObj

# occasionally a char will not be in UTF8,
# this makes sure that all are
def removeNonUnicode(jObj):
	for field in jObj:
		if isinstance(jObj[field],str):
			# jObj[field] = jObj[field].decode('utf-8','ignore')
			jObj[field] = ''.join(i for i in jObj[field] if ord(i)<256)
			if jObj[field] == None:
				jObj[field] = ''
	return jObj


# ALL JSON FIELDS IN AN OBJECT

# archived <class 'bool'>
# author <class 'str'>
# author_flair_css_class <class 'str'>
# author_flair_text <class 'str'>
# body <class 'str'>
# controversiality <class 'int'>
# created_utc <class 'str'>
# distinguished <class 'NoneType'>
# downs <class 'int'>
# edited <class 'bool'>
# gilded <class 'int'>
# id <class 'str'>
# link_id <class 'str'>
# name <class 'str'>
# parent_id <class 'str'>
# retrieved_on <class 'int'>
# score <class 'int'>
# score_hidden <class 'bool'>
# subreddit <class 'str'>
# subreddit_id <class 'str'>
# ups <class 'int'>
# note: distinguished can be
# 			null 		= not distinguished, regular user
# 			moderator 	= moderator (green M)
# 			admin 		= admin (red A)
# 			special 	= special distinguishes

# FULLNAME PREFIXES
# used in fields: link_id, name, parent_id, subreddit_id
# t1 = comment
# t2 = account
# t3 = link
# t4 = message
# t5 = subreddit
# t6 = award
# t8 = promocampaign


###################################
# MySQL general helper functions
###################################

# incrementer class for id fields
# each table class gets one
class Incrementer():
	def __init__(initial=0):
		self.i = initial

	def inc(self):
		self.i += 1
		return self.i

# open connection to database
# then return engine object
def connect(username, password, database):
	db_uri = 'mysql+oursql://{}:{}@{}'.format(username, password, database)
	engine = s.create_engine(db_uri, encoding='utf-8')
	engine.connect()
	return engine


# create a session from the engine
def createSession(eng):
	Session = s.orm.sessionmaker()
	Session.configure(bind=eng)
	session = Session()
	return session

# creates a table class, autoincrementer for each table in the database
def generateTableClasses(eng):
	ABase = automap_base()
	ABase.prepare(eng, reflect=True)

	global Author, Basic_Markup, Post, Discussion, Subreddit, Text
	global author_inc, basic_markup_inc, post_inc, discussion_inc, subreddit_inc, text_inc

	author_inc = Incrementer()
	basic_markup_inc = Incrementer()
	post_inc = Incrementer()
	discussion_inc = Incrementer()
	subreddit_inc = Incrementer()
	text_inc = Incrementer()

	Author = ABase.classes.authors
	Basic_Markup = ABase.classes.basic_markup
	Post = ABase.classes.posts
	Discussion = ABase.classes.discussions
	Subreddit = ABase.classes.subreddits
	Text = ABase.classes.text


####################################
# Single table object tasks
# - operates on a single post object
####################################


# take a single json dictionary object
# load each json field data into the proper table object
# add to session
# pushes to server in main()
# NOTE: must be done in this order, each one inserts a new
# field into the jObj which later functions use
def createTableObjects(jObj, session):
	addSubredditToSession(jObj,session)
	addDiscussionToSession(jObj,session)
	addAuthorToSession(jObj,session)
	addMarkupsAndTextToSession(jObj,session)
	addPostToSession(jObj,session)


# check the dict to see if the subreddit is in the db already
# if not, insert a new subreddit to the session
# if so, simply add an object to jObj: 'subreddit_iac_id'
# use this when inserting the post object
def addSubredditToSession(jObj, session):
	if jObj['subreddit_id'] not in subreddit_dict:
		# example: {'t5_0d032da': 43}
		subreddit_dict[jObj['subreddit_id']] = subreddit_inc.inc()
		subreddit = Subreddit(
			dataset_id 			= reddit_id,
			subreddit_id 		= subreddit_dict[jObj['subreddit_id']],
			subreddit_name 		= jObj['subreddit'],
			subreddit_native_id = jObj['subreddit_id']
			)
		session.add(subreddit)
	jObj['subreddit_iac_id'] = subreddit_dict[jObj['subreddit_id']]


# for our purposes, link and discussion are synonymous
# 	reddit discussions almost always start with link
# 	all top-level comments have that link as their parent
# can't get link title or url without reddit API calls
# so just insert the native id for now
# works basically the same as subreddit
# todo: create a script to run after all insertions to fill in url, title
def addDiscussionToSession(jObj, session):
	if jObj['link_id'] not in link_dict:
		link_dict[jObj['link_id']] = discussion_inc.inc()
		discussion = Discussion(
			dataset_id 			= reddit_id,
			discussion_id 		= link_dict[jObj['link_id']],
			native_discussion_id= jObj['link_id'],
			subreddit_id 		= subreddit_dict[jObj['subreddit_id']]
			)
		session.add(discussion)
	jObj['discussion_iac_id'] = link_dict[jObj['link_id']]


def addAuthorToSession(jObj, session):
	if jObj['author'] not in author_dict:
		author_dict[jObj['author']] = author_inc.inc()
		author = Author(
			dataset_id = reddit_id, 
			author_id  = author_dict[jObj['author']],
			username   = jObj["author"] 
			)
		session.add(author)
	jObj['author_iac_id'] = author_dict[jObj['author']]

# convert markdown body to html tags, making sure to get nested
# then get each tag object
# remove tags and make sure indices of each tag object are correct
# add the inner text to the tag object
# push both the tag objects, cleaned up body text to session
def addMarkupsAndTextToSession(jObj, session):
	# don't need to add text_id in addTextObject()
	# because always have exactly 1 text object
	jObj['text_iac_id'] = text_inc.inc()
	tag_inc = Incrementer()
	body = jObj['body']
	# tempOut.write('\n\n'+jObj['name']+'\n')
	# tempOut.write("___ORIGINAL___:\n"+body+'\n\n')
	body, addedTags = convertAndClean(body)
	# tempOut.write("___TAGS_ADDED___:\n"+body+'\n\n')
	tObjs = getAllTagObjects(body, tag_inc)
	# to keep track of if we're still getting more tags
	new_tObjs = tObjs
	while len(new_tObjs) != 0:
		orig_tObjs, body = stripTagsAndFixStartEnd(tObjs, body)
		# tempOut.write("___NEW___:\n"+body+'\n\n')
		# [tempOut.write(str(tObj)+"\n") for tObj in sorted(tObjs, key=lambda k: k['start'])]
		# try to get more tags in case we have nested quotes or some such
		new_tObjs = getAllTagObjects(body, tag_inc)
		tObjs = orig_tObjs + new_tObjs
	tObjs = addTextToTagObjects(tObjs, body)
	tObjs = groupTagObjects(tObjs)
	for tObj in tObjs:
		addTagObjectToSession(tObj, jObj, session)
	jObj['newBody'] = body
	# tempOut.write("___TAGS_REMOVED___:\n"+body+'\n\n')
	addTextObjectToSession(jObj, session)

def addTextObjectToSession(jObj, session):
	# text_id = text_inc.inc()
	# jObj['text_iac_id'] = text_id
	text = Text(
		dataset_id 	= reddit_id,
		text_id 	= jObj['text_iac_id'],
		text 		= jObj['newBody'].encode(encoding='utf8')
		)
	session.add(text)
	
def addTagObjectToSession(tObj, jObj, session):
	if tObj['start'] > tObj['end']:
		print("warning: start index > end index for tag in post",jObj['name'],"with tag id",tObj['id'])
	if tObj['start'] < 0:
		print("warning: start index < 0 for tag in post",jObj['name'],"with tag id",tObj['id'])
	# this is a hack
	if tObj['end'] >= 0 and tObj['start'] >= 0:	
		basic_markup = Basic_Markup(
			dataset_id 		= reddit_id,
			text_id 		= jObj['text_iac_id'],
			# markup_id auto increments by itself in MySQL server
			start 			= tObj['start'],
			end 			= tObj['end'],
			type_name		= tagToType[tObj['type']],
			markup_group_id = tObj['group']
			)
		if tObj['url'] != None:
			basic_markup.attribute_str = '{"href": "'+tObj['url']+'"}'
		session.add(basic_markup)

def addPostToSession(jObj, session):
	ts = datetime.datetime.fromtimestamp(
			int(jObj['created_utc'])
			).strftime('%Y-%m-%d %H:%M:%S')
	if jObj['name'] not in post_dict:
		post_dict[jObj['name']] = post_inc.inc()
	parent_id = None
	# t3 prefix means parent is comment, not link or subreddit
	if jObj['parent_id'][:2] == 't3':
		if jObj['parent_id'] not in post_dict:
			post_dict['parent_id'] = post_inc.inc()
		parent_id = post_dict['parent_id']
	post = Post(
		dataset_id 			= reddit_id,
		discussion_id 		= jObj['discussion_iac_id'],
		post_id 			= post_dict[jObj['name']],
		author_id 			= jObj['author_iac_id'],
		timestamp			= ts,
		parent_post_id		= parent_id,
		native_post_id  	= jObj['name'],
		text_id				= jObj['text_iac_id'],
		# parent_relation_id 	= 
		# votes				=
		)
	session.add(post)
	

####################################
# 	Markup Helper Functions
####################################


# regex grabs markdown groups for each type
markRe = {
	'italic':			r'(?<!\*)([\*][^\*]+[\*])(?!\*)',
	# stuff like ****CRASH****
	'multiAsterisk':	r'(\*{3,}[^\*]+\*{3,})',		
	'bold':				r'(\*{2}[^\*]+\*{2})',
	'strikethrough': 	r'(\~{2}[^\*]+\~{2})',
	'quote':			r'(&gt;[^\*\n]+\n)',
	'link':				r'(\[.*\]\([^\)\s]+\))',
	'header':			r'(\#+.+\s)',
	# unordered list item
	'ulist':			r'([\*\+\-] .*\n)',
	# ordered list item
	'olist':			r'([0-9]+\. .*\n)',
	'supPar':			r'(\^\([^\)]*?\))',
	'superscript':		r'(\^\\?[^\s\<\>\[\]\)\(]+)(?=[\s\n\<\>\]\[\)\(])?',
}

# same as above but for html tags instead
tagRe = {
	'em':				r'(\<em\>[\s\S]+?\<\/em\>)',
	'strong':			r'(\<strong\>[\s\S]+?\<\/strong\>)',
	'strike': 			r'(\<strike\>[\s\S]+?\<\/strike\>)',
	'blockquote':		r'(\<blockquote\>[\s\S]+?\<\/blockquote\>)',
	'link':				r'(?i)(<a[^>]+?>[\s\S]+?</a>)',
	'h1':				r'(\<h1\>[\s\S]*?\<\/h1\>)',
	'h2':				r'(\<h2\>[\s\S]*?\<\/h2\>)',
	'h3':				r'(\<h3\>[\s\S]*?\<\/h3\>)',
	'h4':				r'(\<h4\>[\s\S]*?\<\/h4\>)',
	'h5':				r'(\<h5\>[\s\S]*?\<\/h5\>)',
	'h6':				r'(\<h6\>[\s\S]*?\<\/h6\>)',
	'ul':				r'(\<ul\>[\s\S]+?\<\/ul\>)',
	'ol':				r'(\<ol\>[\s\S]+?\<\/ol\>)',
	'li':				r'(\<li\>[\s\S]+?\<\/li\>)',
	'sup':				r'(\<sup\>[\s\S]+?\<\/sup\>)',
	'pre':				r'(\<pre\>[\s\S]+?\<\/pre\>)',
	'code':				r'(\<code\>[\s\S]+?\<\/code\>)',
	'asterisks':		r'(\<asterisks\>[\s\S]+?\<\/asterisks\>)',
	'del':				r'(\<del\>[\s\S]+?\<\/del\>)',
	'table':			r'(\<table\>[\s\S]+?\<\/table\>)',
	'thead':			r'(\<thead\>[\s\S]+?\<\/thead\>)',
	'tbody':			r'(\<tbody\>[\s\S]+?\<\/tbody\>)',
	'tr':				r'(\<tr\>[\s\S]+?\<\/tr\>)',
	'td':				r'(?i)(<td[^>]*?>.*?</td>)',
	'th':				r'(?i)(<th[^>]*?>.*?</th>)',

}

# html tag names -> MySQL type names (to match IAC)
tagToType = {
	'em':				'italic',
	'strong':			'bold',
	'strike': 			'strikethrough',
	'blockquote':		'quote',
	'link':				'link',
	'h1':				'header1',
	'h2':				'header2',
	'h3':				'header3',
	'h4':				'header4',
	'h5':				'header5',
	'h6':				'header6',
	'ul':				'unorderList',
	'ol':				'orderedList',
	'li':				'listItem',
	'sup':				'superscript',
	'supP':				'superscript',
	'pre':				'pre',
	'code':				'code',
	'asterisks':		'boldAndItalic',
	'del':				'deleted',
	'table':			'table',
	'thead':			'tableHead',
	'tbody':			'tableBody',
	'th':				'tableHeadCell',
	'tr':				'tableRow',
	'td':				'tableCell',
}

# markdown -> html tags
def convertAndClean(body):
	newbody = body + ""
	newbody = newbody.replace('&nbsp;',' ')
	newbody = newbody.replace('&#39;',"'")
	newbody = newbody.replace('&quot;','"')
	newbody = newbody.replace('&gt;','>')
	newbody = newbody.replace('&lt;','<')
	newbody = newbody.replace('&amp;','&')
	newbody = markdown(newbody)
	newbody = newbody.replace('&nbsp;',' ')
	newbody = newbody.replace('&#39;',"'")
	newbody = newbody.replace('&quot;','"')
	newbody = newbody.replace('&gt;','>')
	newbody = newbody.replace('&lt;','<')
	newbody = newbody.replace('&amp;','&')
	newbody = newbody.replace('<p>','')
	newbody = newbody.replace('</p>','')
	newbody = newbody.replace('<hr />', '')
	newbody = newbody.replace('<hr/>', '')
	newbody = newbody.replace('<hr>','')
	newbody = newbody.replace('<br />', '')
	newbody = newbody.replace('<br/>', '')
	newbody = newbody.replace('<br>','')
	newbody = fixEmptyLinkTags(newbody)
	newbody = fixFalseEmTags(newbody)
	# to check if we actually changed anything
	addedTags = body != newbody
	return newbody, addedTags

# sometimes get stuff like '<a href="/subreddit"></a>'
# has nothing inside the tags, but shows up as '/subreddit'
# this adds the link to the inner content of the tags
def fixEmptyLinkTags(body):
	newbody = body
	emptyLinkRe = r'(?i)(<a[^>]+?></a>)'
	urlRe = r'\<a href\=\"(.+)\"\>'
	matchObjs = re.finditer(emptyLinkRe,body)
	for obj in matchObjs:
		# <a href="/link"></a>
		bothTags = obj.group()
		# /link in above
		urlmatches = re.findall(urlRe,bothTags)
		if len(urlmatches)>0:
			url = urlmatches[0]
			# replace bothTags with <a href="/link">/link</a>
			newBothTags = bothTags.replace('"></a>','">'+url+'</a>')
			# now put it back into the body
			newbody = newbody.replace(bothTags,newBothTags)
	return newbody

# extreme corner case:
# ....blah blah blah!*
# ^*blah ^blah ^blah
# this is not an italic, but mistune, markdown2 think it is
def fixFalseEmTags(body):
	falseEmRe = r'(\<em\>(?:[^<]*?(?!</em>)\n+)[\s\S]*?\<\/em\>)'
	newbody = body
	matchObjs = re.finditer(falseEmRe,body)
	for obj in matchObjs:
		newObjText = obj.group().replace('<em>','')
		newObjText = obj.group().replace('</em>','')
		newbody = newbody.replace(obj.group(),newObjText)
	return newbody

# in: body text (after replacing markup with tags)
# out: list of dicts (tag objects)
def getAllTagObjects(body, tag_inc):
	tObjs = []
	for tag in tagRe:
		matches = re.finditer(tagRe[tag], body)
		for m in matches:
			tObjs.append(matchToTagObject(m, tag, body, tag_inc))
	return tObjs

# converts re's MatchObject to a tag object
def matchToTagObject(match, tag, body, tag_inc):
	tObj = {
		'type': 		tag,
		'start':		match.start(),
		'end':			match.end(),
		# only used for link tags
		'url': 			None,
		'text':			None,
		# 'processed':	False,
		'group':		None,
		'id':			tag_inc.inc(),
		'tagRemoved':	False,
		# how many times it's been through the stripTags loop
		'generation':	0,
		'origText':		match.group(),
		'style': 		None,
	}
	if tag == 'link':
		tagText = body[tObj['start']:tObj['end']]
		firstTag = re.findall(r'(?i)(<a[^>]+>)', tagText)[0]
		tObj['url'] = firstTag[9:-2]
	if tag == 'td':
		tagText = body[tObj['start']:tObj['end']]
		match = re.findall(r'(?i)(<td[^>]+>)', tagText)
		if len(match) > 0:
			firstTag = match[0]
			tObj['style'] = firstTag[11:-2]
	if tag == 'th':
		tagText = body[tObj['start']:tObj['end']]
		match = re.findall(r'(?i)(<th[^>]+>)', tagText)
		if len(match) > 0:
			firstTag = match[0]
			tObj['style'] = firstTag[11:-2]
	return tObj

# maybe the most frustrating bit of code I've written
# takes list of tag objects, removes their tags from the body, 
# and fixes their start,end positions to account for missing tags
def stripTagsAndFixStartEnd(tObjs, body):
	newbody = body
	newTags = sorted([t for t in tObjs if not t['tagRemoved']], key=lambda k: k['start'])
	oldTags = sorted([t for t in tObjs if t['tagRemoved']], key=lambda k: k['start'])
	r = 0
	for _ in range(len(newTags)):
		tObj = newTags.pop(0)
		newbody, rO, rC = stripTag(tObj, newbody)
		tObj['tagRemoved'] = True
		r += rO+rC
		# tempOut.write("text: "+tObj['origText']+"\n open size: "+str(rO)+" closedsize: "+str(rC))
		# tempOut.write(" orig start: "+str(tObj['start'])+" orig end: "+str(tObj['end'])+"\n")
		for old in oldTags:
			# from a previous generation of tags
			if old['generation'] > 0:
				# if this old tag is nested, only remove opening tag
				if old['start'] > tObj['start'] and old['end'] <= tObj['end']:
					old['start'] -= rO
					old['end'] -= rO
				# if tObj nested in old tag
				elif old['start'] <= tObj['start'] and old['end'] >= tObj['end']:
					old['end'] -= rC+rO
				# if old is strictly after tObj
				elif old['start'] >= tObj['end']:
					old['start'] -= rO+rC
					old['end'] -= rO+rC
			# if the old tag is from this generation, we know it is not nested
			# because sorting by start means higher level tags come first
			# therefore only end position needs modification
			else:
				if old['end'] >= tObj['end']:
					old['end'] -= rO
				if old['end'] > tObj['start']:
					old['end'] -= rC
		for new in newTags:
			# these should all be either nested inside tObj
			# or come after, none should envelope tObj
			if new['start'] < tObj['end']: # nested
				new['start'] -= rO
				new['end'] -= rO
			else: # not nested
				new['start'] -= rO+rC
				new['end'] -= rO+rC
		tObj['end'] -= (rO+rC)
		# tempOut.write(" fixed end: "+str(tObj['end'])+" text length: "+str(tObj['end']-tObj['start'])+"\n")
		oldTags.append(tObj)
	for tObj in oldTags:
		tObj['generation'] += 1
	return oldTags, newbody

# given # of chars, position the open/close tags take up, 
# remove those chars from the body
def stripTag(tObj, body):
	newbody = body
	s = tObj['start']
	e = tObj['end']
	# size of open tag, close tag <></>
	o = len(tObj['type'])+2
	c = len(tObj['type'])+3
	if tObj['type'] == 'link':
		# link: <a href=""></a>
		o = len(tObj['url'])+11
		c = 4
	elif tObj['type'] == 'td' or tObj['type'] == 'th':
		if tObj['style'] != None:
			o = len(tObj['style'])+13
			c = 5
		
	# remove end tag first because indices count from start of string
	newbody = newbody[0:e-c] + newbody[e:]
	newbody = newbody[0:s] + newbody[s+o:]
	return newbody, o, c

# text inside markup added to each tag object
def addTextToTagObjects(tObjs, body):
	for tObj in tObjs:
		tObj['text'] = body[tObj['start']:tObj['end']]
	return tObjs

# for lists, quotes, superscripts
def groupTagObjects(tObjs):
	tObjs = sorted(tObjs, key=lambda k: k['start'])
	for tObj in tObjs:
		tObj['group'] = None
	currGroup = 1
	grouped = []
	for i in range(len(tObjs)):
		t = tObjs.pop(0)
		if t['group'] == None:
			t['group'] = currGroup
			if t['type'] in ['ul', 'ol']:
				for i in tObjs:
					if (i['start'] >= t['start']
					and i['end'] <= t['end']
					and i['type'] == 'li'):
						i['group'] = t['group']
			elif t['type'] in ['sup','blockquote']:
				for i in tObjs:
					if (i['start'] >= t['start']
					and i['end'] <= t['end']
					and i['type'] == t['type']):
						i['group'] = t['group']
			elif t['type'] == 'table':
				for i in tObjs:
					if (i['start'] >= t['start']
					and i['end'] <= t['end']
					and i['type'] in ['thead', 'th', 'tbody', 'tr', 'td']):
						i['group'] = t['group']
			currGroup += 1
		grouped.append(t)
	return grouped


###################################
# Execution starts here
###################################

def main(user=sys.argv[1],pword=sys.argv[2],db=sys.argv[3],dataFile=sys.argv[4]):

	# if len(sys.argv) != 5:
	# 	print("Incorrect number of arguments given")
	# 	print("Usage: python getRawJSON [username] [password] [host/database name] [JSON data file]")
	# 	print("Example: python getRawJSON root password localhost/iac sampleComments")
	# 	sys.exit(1)

	print('Connecting to database',db,'as user',user)
	eng = connect(user, pword, db)
	metadata = s.MetaData(bind=eng)
	session = createSession(eng)
	generateTableClasses(eng)
	print('Loading data from',dataFile)
	with open(dataFile,'r', encoding='utf-8') as data:
		jObjs = []
		comment_index = 1
		for line in data:
			jObj = jsonLineToDict(line)
			jObjs.append(jObj)
			if len(jObjs) >= batch_size:
				for jObj in jObjs:
					createTableObjects(jObj,session)
				print("Pushing comments up to",comment_index)
				sys.stdout.flush()
				if comment_index > 12035000:
					session.commit()
				else:
					# effectively throw away comments until we're up to where we left off
					session = createSession(eng)
				jObjs = []
			comment_index += 1
	session.commit()

if __name__ == "__main__":
	main()
