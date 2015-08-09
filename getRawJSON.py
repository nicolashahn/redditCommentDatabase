# NLDS Lab
# Nicolas Hahn
# A script to take raw Reddit JSON data 
# and insert it to a MySQL DB based on IAC schema
# input: Raw Reddit JSON post objects in text format, one object per line
# output: MySQL insertions for each object according to schema
# the 1 month dataset has 53,851,542 comments total

import json
import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.dialects import mysql
import sys
import re
import markdown2 as md
import datetime

###################################
# Global variables
###################################

# because 1-5 appear to be taken in IAC
reddit_id = 6

# {native_id: db_id}
# so we don't have to query to check if link/subreddit obj already exists
link_dict = {}
subreddit_dict = {}
author_dict = {}
post_dict = {}

# temporary output file for checking things 
# (print statements choke on unicode)
tempOut = open('tempOut','w', encoding='utf8')


###################################
# JSON data manipulation
###################################

# json text dump -> list of json-dicts
# also encodes the line number the object in the raw file
def jsonDataToDict(data):
	jObjs = []
	i = 0
	for line in data:
		i += 1
		jline = json.loads(line)
		jline['line_no'] = i
		jObjs.append(jline)
		# print([x+": "+str(jline[x]) for x in sorted(jline)])
	return jObjs


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
	def __init__(self):
		# 0 so that inc() returns 1 the first time
		self.i = 0

	def inc(self):
		self.i += 1
		return self.i

	def reset(self):
		self.i = -1

# open connection to database
# then return engine object
def connect(username, password, database):
	db_uri = 'mysql://{}:{}@{}'.format(username, password, database)
	engine = s.create_engine(db_uri)
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
	Text = ABase.classes.texts


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
	body = jObj['body']
	addedTags = True
	# keep adding tags until all markup replaced
	while addedTags == True:
		body, addedTags = convertAndClean(body)
	tempOut.write(jObj['name']+'\n')
	tempOut.write("___OLD___:\n"+body+'\n\n')
	tObjs = getAllTagObjects(body)
	# to keep track of if we're still getting more tags
	new_tObjs = tObjs
	while len(new_tObjs) != 0:
		# tempOut.write("tObjs:\n"+str(tObjs)+"\n\n")
		orig_tObjs, body = stripAllTagsAndFixStartEnd(tObjs, body)
		tempOut.write("___NEW___:\n"+body+'\n\n')
		# tempOut.write("tObjs:\n"+str(fixedTOb/js)+"\n\n\n\n")
		# try to get more tags in case we have nested quotes or some such
		new_tObjs = getAllTagObjects(body)
		print('new tags:', new_tObjs)
		tObjs = orig_tObjs + new_tObjs
	tObjs = addTextToTagObjects(tObjs, body)
	for tObj in tObjs:
		addTagObjectToSession(tObj, jObj, session)
	jObj['newBody'] = body
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
	attributeObj = {}
	if tObj['url'] != None:
		attributeObj['href'] = tObj['url']
	basic_markup = Basic_Markup(
		dataset_id 		= reddit_id,
		text_id 		= jObj['text_iac_id'],
		# markup_id 		= basic_markup_inc.inc(),
		start 			= tObj['start'],
		end 			= tObj['end'],
		type_name		= tagToType[tObj['type']],
		# attribute_str	= attributeObj
		)
	session.add(basic_markup)

def addPostToSession(jObj, session):
	ts = datetime.datetime.fromtimestamp(
			int(jObj['created_utc'])
			).strftime('%Y-%m-%d %H:%M:%S')
	if jObj['name'] not in post_dict:
		post_dict[jObj['name']] = post_inc.inc()
	# if the parent_id is a comment (not a link or subreddit)
	parent_id = None
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
	# need to add \n lookbehind to most of these
	'italic':			r'(?<!\*)([\*][^\*]+[\*])(?!\*)',
	'bold':				r'(\*{2}[^\*]+\*{2})',
	'strikethrough': 	r'(\~{2}[^\*]+\~{2})',
	'quote':			r'(&gt;[^\*\n]+\n)',
	# links are tricky, keeps grabbing spaces as well - not finished
	'link':				r'(\[.*\]\([^\)\s]+\))',
	'header':			r'(\#+.+\s)',
	# unordered list item
	'ulist':			r'([\*\+\-] .*\n)',
	# ordered list item
	'olist':			r'([0-9]+\. .*\n)',
	'superscript':		r'(\^[^\s\n\<\>\]\[\)\(]+)(?=[\s\n\<\>\]\[\)\(])?',
}

# same as above but for html tags instead
tagRe = {
	'em':				r'(\<em\>[\s\S]+?\<\/em\>)',
	'strong':			r'(\<strong\>[\s\S]+?\<\/strong\>)',
	'strike': 			r'(\<strike\>[\s\S]+?\<\/strike\>)',
	'blockquote':		r'(\<blockquote\>[\s\S]+?\<\/blockquote\>)',
	'link':				r'(?i)(<a[^>]+?>.*?</a>)',
	'h1':				r'(\<h1\>[\s\S]+?\<\/h1\>)',
	'h2':				r'(\<h2\>[\s\S]+?\<\/h2\>)',
	'h3':				r'(\<h3\>[\s\S]+?\<\/h3\>)',
	'h4':				r'(\<h4\>[\s\S]+?\<\/h4\>)',
	'h5':				r'(\<h5\>[\s\S]+?\<\/h5\>)',
	'h6':				r'(\<h6\>[\s\S]+?\<\/h6\>)',
	'ul':				r'(\<ul\>[\s\S]+?\<\/ul\>)',
	'ol':				r'(\<ol\>[\s\S]+?\<\/ol\>)',
	'li':				r'(\<li\>[\s\S]+?\<\/li\>)',
	'sup':				r'(\<sup\>[\s\S]+?\<\/sup\>)',
	'pre':				r'(\<pre\>[\s\S]+?\<\/pre\>)',
	'code':				r'(\<code\>[\s\S]+?\<\/code\>)',
}

# html tag names -> MySQL type names
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
	'pre':				'pre',
	'code':				'code',
}

# markdown -> html tags
def convertAndClean(body):
	newbody = body.replace('&gt;','>')
	newbody = newbody.replace('&amp;','&')
	newbody = newbody.replace('&lt;','<')
	newbody = replaceSuperscriptTags(newbody)
	newbody = md.markdown(newbody)
	newbody = newbody.replace('<p>','')
	newbody = newbody.replace('</p>','')
	newbody = replaceStrikethroughTags(newbody)
	addedTags = body != newbody
	return newbody, addedTags

# markdown2 replaces all Reddit markdown except strikethrough, superscript
# so do it here manually
def replaceStrikethroughTags(body):
	newbody = body
	matchObjs = re.finditer(markRe['strikethrough'],body)
	for obj in matchObjs:
		newObjText = '<strike>' + obj.group()[2:-2] + '</strike>'
		newbody = newbody.replace(obj.group(), newObjText)
	return newbody

def replaceSuperscriptTags(body):
	newbody = body
	matchObjs = re.finditer(markRe['superscript'],body)
	for obj in matchObjs:
		newObjText = '<sup>' + obj.group()[1:] + '</sup>'
		newbody = newbody.replace(obj.group(),newObjText)
	return newbody

# in: body text (after replacing markup with tags)
# out: list of dicts (tag objects)
def getAllTagObjects(body):
	tObjs = []
	for tag in tagRe:
		matches = re.finditer(tagRe[tag], body)
		for m in matches:
			tObjs.append(matchToTagObject(m, tag, body))
	return tObjs

# converts re's MatchObject to a tag object
def matchToTagObject(match, tag, body):
	tObj = {
		'type': 	tag,
		'start':	match.start(),
		'end':		match.end(),
		'url': 		None,
		'text':		None,
		'processed':False,
	}
	if tag == 'link':
		tagText = body[tObj['start']:tObj['end']]
		firstTag = re.findall(r'(?i)(<a[^>]+>)', tagText)[0]
		tObj['url'] = firstTag[9:-2]
	return tObj

# gnarly and ugly, but seems to work
def stripAllTagsAndFixStartEnd(tObjs, body):
	newbody = body
	# r = how many characters we've already removed
	r = 0
	fixed = []
	# sort by original start position
	tObjs = sorted(tObjs, key=lambda k: k['start'])
	for i in range(len(tObjs)):
		tObj = tObjs.pop(0)
		if tObj['processed'] == False:
			oldEnd = tObj['end']
			tObj['start'] -= r
			tObj['end'] -= r
			# tempOut.write('\n\n\nITERATION '+str(i)+'\n'+tObj['type']+' '+str(tObj['start'])+' '+str(tObj['end'])+'\n')
			# tempOut.write(newbody[tObj['start']:tObj['end']]+'\n\n\n\n')
			# tempOut.write(newbody)
			# if tObj['type'] != 'link':
			# removeO, C = how many characters the opening, closing tags take
			newbody, removeO, removeC = stripTag(tObj, newbody)
			tObj['end'] -= removeO+removeC
			r += removeO
			# deal with nested tags:
			# if some tag in fixed envelopes this tObj
			# subtract how much we just removed from its end position
			for f in fixed:
				if f['end'] > tObj['end']:
					f['end'] -= removeO+removeC
			# if we have nested tag later in the list
			# add the closing tag size to offset when we subtract it later
			for t in tObjs:
				if t['start'] <= oldEnd:
					t['start'] += removeC
					t['end'] += removeC
			r += removeC
			tObj['processed'] = True
			fixed.append(tObj)
	return fixed, newbody

# given # of chars, position the open/close tags take up, 
# remove those chars from the body
def stripTag(tObj, body):
	newbody = body
	s = tObj['start']
	e = tObj['end']
	if tObj['type'] != 'link':
		# size of open tag, close tag
		o = len(tObj['type'])+2
		c = len(tObj['type'])+3
	else:
		# link: <a href=""></a>
		o = len(tObj['url'])+11
		c = 4
	# remove end tag first because indices count from start of string
	newbody = newbody[0:e-c] + newbody[e:]
	newbody = newbody[0:s] + newbody[s+o:]
	return newbody, o, c

def addTextToTagObjects(tObjs, body):
	for tObj in tObjs:
		tObj['text'] = body[tObj['start']:tObj['end']]
	return tObjs

###################################
# Execution starts here
###################################

def main():

	if len(sys.argv) != 5:
		print("Incorrect number of arguments given")
		print("Usage: python getRawJSON [username] [password] [JSON data file] [host/database name]")
		print("Example: python getRawJSON root password sampleComments localhost/iac")
		sys.exit(1)

	user = sys.argv[1]
	pword = sys.argv[2]
	data = sys.argv[3]
	db = sys.argv[4]
	
	data = open(data,'r', encoding='utf8')
	jObjs = jsonDataToDict(data)
	eng = connect(user, pword, db)
	metadata = s.MetaData(bind=eng)
	session = createSession(eng)
	generateTableClasses(eng)

	# show all fields + types
	# [print(x, jObjs[8][x].__class__) for x in sorted(jObjs[8])]

	# show fields with actual example values
	# [print(x, jObjs[8][x]) for x in sorted(jObjs[8])]

	for jObj in jObjs:
		createTableObjects(jObj,session)
		session.commit()

if __name__ == "__main__":
	main()