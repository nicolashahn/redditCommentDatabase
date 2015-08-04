# NLDS Lab
# Nicolas Hahn
# A script to take raw Reddit JSON data and insert it into a MySQL database
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


###################################
# JSON data manipulation
###################################

# json text dump -> list of json-dicts
# also encodes the line number the object in the raw file
def jsonDataToDict(data):
	jobjs = []
	i = 0
	for line in data:
		i += 1
		jline = json.loads(line)
		jline['line_no'] = i
		jobjs.append(jline)
		# print([x+": "+str(jline[x]) for x in sorted(jline)])
	return jobjs


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

	global Author, Basic_Markup, Post, Discussion, Subreddit
	global author_inc, basic_markup_inc, post_inc, discussion_inc, subreddit_inc

	author_inc = Incrementer()
	basic_markup_inc = Incrementer()
	post_inc = Incrementer()
	discussion_inc = Incrementer()
	subreddit_inc = Incrementer()

	Author = ABase.classes.authors
	Basic_Markup = ABase.classes.basic_markup
	Post = ABase.classes.posts
	Discussion = ABase.classes.discussions
	Subreddit = ABase.classes.subreddits


####################################
# Single table object tasks
# - operates on a single post object
####################################


# take a single json dictionary object
# load each json field data into the proper table object
# add to session
# pushes to server in main()
def createTableObjects(jobj, session):

	# addSubredditToSession(jobj,session)
	# addDiscussionToSession(jobj,session)
	# addAuthorToSession(jobj,session)
	addMarkupsToSession(jobj,session)
	# addTextToSession(jobj,session)
	# addPostToSession(jobj,session)


# check the dict to see if the subreddit is in the db already
# if not, insert a new subreddit to the session
# if so, simply add an object to jobj: 'subreddit_iac_id'
# use this when inserting the post object
def addSubredditToSession(jobj, session):
	if jobj['subreddit_id'] not in subreddit_dict:
		# example: {'t5_0d032da': 43}
		subreddit_dict[jobj['subreddit_id']] = subreddit_inc.inc()
		subreddit = Subreddit(
			dataset_id 			= reddit_id,
			subreddit_id 		= subreddit_dict[jobj['subreddit_id']],
			subreddit_name 		= jobj['subreddit'],
			subreddit_native_id = jobj['subreddit_id']
			)
		session.add(subreddit)
	jobj['subreddit_iac_id'] = subreddit_dict[jobj['subreddit_id']]

# for our purposes, link and discussion are synonymous
# 	reddit discussions almost always start with link
# 	all top-level comments have that link as their parent
# can't get link title or url without reddit API calls
# so just insert the native id for now
# works basically the same as subreddit
# todo: create a script to run after all insertions to fill in url, title
def addDiscussionToSession(jobj, session):
	if jobj['link_id'] not in link_dict:
		link_dict[jobj['link_id']] = discussion_inc.inc()
		discussion = Discussion(
			dataset_id 			= reddit_id,
			discussion_id 		= link_dict[jobj['link_id']],
			native_discussion_id= jobj['link_id'],
			subreddit_id 		= subreddit_dict[jobj['subreddit_id']]
			)
		session.add(discussion)
	jobj['discussion_iac_id'] = link_dict[jobj['link_id']]


def addAuthorToSession(jobj, session):
	if jobj['author'] not in author_dict:
		author_dict[jobj['author']] = author_inc.inc()
		author = Author(
			dataset_id = reddit_id, 
			author_id  = author_dict[jobj['author']],
			username   = jobj["author"] 
			)
		session.add(author)
	jobj['author_iac_id'] = author_dict[jobj['author']]




def addPostToSession(jobj, session):
	# post = Post(
	# 	dataset_id = reddit_id,
	# 	discussion_id = 
	# 	)
	pass


####################################
# Markup
# - get each instance of markup
# 	- each time a bit of text is italic/bold/strikethough/etc
# - turn into a basic_markup table object
# - add to session
####################################

# type of markup: regex to grab group
markRe = {
	'italic':	r'(?<!\*)([\*][^\*]+[\*])(?!\*)',
	'bold':		r''
}


# create a markup table object
# for each slice of marked up text in the 'body' field
# add to session
def addMarkupsToSession(jobj, session):
	print(jobj['name'])
	body = jobj['body']
	allMarkups = []
	allMarkups += addMarkupObjectFromType("italic",markRe['italic'],body,session)
	for m in allMarkups:
		print("   ",m.group())
		print("   ",m.start(), m.end())
	# subscript

# helper for the add(markup type) functions
# given a markup symbol (*),(**),(~), etc
# return a list of dicts:
# 	text: inside the markup (including markup symbols): 	(str)
# 	start: the start position: 								(int)
# 	end: the end position:									(int)
def addMarkupObjectFromType(type, regex, body, session):
	matchObjs = re.finditer(regex,body)
	return(matchObjs)
	# todo:
	# get start and end point of each mark
	# create a Basic_Markup object for each
	# add to server




###################################
# Execution starts here
###################################

def main():

	if len(sys.argv) != 5:
		print("Incorrect number of arguments given")
		print("Usage: python getRawJSON [username] [password] [JSON data file] [host/database name]")
		print("Example: python getRawJSON root password sampleComments localhost/reddit")
		sys.exit(1)

	user = sys.argv[1]
	pword = sys.argv[2]
	data = sys.argv[3]
	db = sys.argv[4]
	
	# raw text -> json dicts
	data = open(data,'r',)
	jobjs = jsonDataToDict(data)

	# connect to server, bind metadata, create session
	eng = connect(user, pword, db)
	metadata = s.MetaData(bind=eng)
	session = createSession(eng)

	# creates a table class and autoincrementer for each table in the database
	generateTableClasses(eng)

	# uncomment to show all fields + types
	# [print(x, jobjs[8][x].__class__) for x in sorted(jobjs[8])]

	# show fields with actual example values
	# [print(x, jobjs[8][x]) for x in sorted(jobjs[8])]


	# now ready to start inserting to database
	for jobj in jobjs:
		# if jobj['line_no'] == 21:
		# 	addMarkupObjects(jobj, session)
		createTableObjects(jobj,session)
		# finally, commit all table object to database
		session.commit()

	
		

if __name__ == "__main__":
	main()