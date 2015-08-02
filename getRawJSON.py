# NLDS Lab
# Nicolas Hahn
# A script to take raw Reddit JSON data and insert it into a MySQL database
# input: Raw Reddit JSON post objects in text format, one object per line
# output: MySQL insertions for each object according to schema
# note to self: the 1 month dataset has 53,851,542 comments total, plan accordingly

import json
import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
import sys
import re


###################################
# Global variables
###################################

# create base table class
Base = declarative_base()

# because 1-5 appear to be taken in IAC
reddit_id = 6

###################################
# JSON data manipulation
###################################

# json text dump -> list of json-dicts
def jsonDataToDict(data):
	jobjs = []
	for line in data:
		jline = json.loads(line)
		jobjs.append(jline)
		# print([x+": "+str(jline[x]) for x in sorted(jline)])
	return jobjs


###################################
# MySQL general helper functions
###################################

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

# auto-incrementer class for id fields
# each table class gets one
class AutoInc():
	def __init__(self):
		self.i = 0

	def inc(self):
		self.i += 1
		return self.i

	def reset(self):
		self.i = 0

####################################
# Table Classes
####################################

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


class Author(Base):
	__tablename__ = 'authors'
	authorInc = AutoInc()

	dataset_id = s.Column(mysql.TINYINT(), primary_key=True)
	author_id = s.Column(mysql.INTEGER(), primary_key=True, default=authorInc.inc())
	# example schema has username as 255 chars - seems like too many
	username = s.Column(mysql.VARCHAR(30))

class Basic_Markup(Base):
	__tablename__ = 'basic_markup'
	markupInc = AutoInc()

	dataset_id = s.Column(mysql.TINYINT(), primary_key=True)
	text_id = s.Column(mysql.INTEGER())
	markup_id = s.Column(mysql.INTEGER(), primary_key=True, default=markupInc.inc())
	start = s.Column(mysql.INTEGER())
	end = s.Column(mysql.INTEGER())
	type_name = s.Column(mysql.VARCHAR(20))
	attribute_str = s.Column(mysql.TEXT())



####################################
# Single table object tasks
# - operates on a single post object
####################################

# take a single json dictionary object
# load each json field data into the proper table object
# add to session, push to db after all are added
def createTableObjects(jobj, session):
	createAuthorTableObject(jobj,session)
	# finally, commit all table object to database
	session.commit()

def createAuthorTableObject(jobj, session):
	author = Author(
		dataset_id = reddit_id, 
		# sqlalchemy auto-increments primary keys by default
		# author_id = 
		username   = jobj["author"] 
		)
	session.add(author)

####################################
# Markup
# - get each instance of markup
# 	- each time a bit of text is italic/bold/strikethough/etc
# - turn into a basic_markup table object
# - add to session
####################################

# create a markup table object
# for each slice of marked up text in the 'body' field
# add to session
def addMarkup(jobj, session):
	body = jobj['body']
	addItalics(body,session)
	addBolds(body,session)
	addStrikethroughs(body,session)
	addQuotes(body,session)

def addItalics(body,session):
	pass

def addBolds(body,session):
	pass

def addStrikethroughs(body,session):
	pass

def addQuotes(body,session):
	pass


###################################
# Program starts here
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

	# uncomment to show all fields + types
	[print(x, jobjs[8][x].__class__) for x in sorted(jobjs[8])]

	# show fields with actual example values
	# [print(x, jobjs[8][x]) for x in sorted(jobjs[8])]
	# what type is 'distinguished'? it's always null, probably bool

	

	# now ready to start inserting to database
	for jobj in jobjs:
		createTableObjects(jobj,session)
	

if __name__ == "__main__":
	main()