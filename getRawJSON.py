# Nicolas Hahn
# in: Raw Reddit JSON post objects in text format, one object per line
# out: MySQL insertions for each object according to schema

import json
import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
import sys


###################################
# Global variables
###################################

# create base table class
Base = declarative_base()

# because 1-5 appear to be taken in IAC
reddit_id = 6

# for auto-incrementer
autoinc = 0

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
# MySQL setup helper functions
###################################

# open connection to database
# then return engine object
def connect(username, password, database):
	db_uri = 'mysql://{}:{}@{}'.format(username, password, database)
	engine = s.create_engine(db_uri)
	engine.connect()
	return engine

# dataset = tinyint(3)
# id = integer(20)
# username = varchar(255)
# def createAuthor(dataset, id, username):
# 	pass

# have python do the auto-incrementation
def autoIncrement():
	global autoinc
	autoinc += 1
	return autoinc

def resetAutoIncrement():
	autoinc = 0

####################################
# Table Classes
####################################

class Author(Base):
	__tablename__ = 'authors'

	dataset_id = s.Column(mysql.TINYINT(3), primary_key=True)
	author_id = s.Column(mysql.INTEGER(20), primary_key=True, default=autoIncrement)
	username = s.Column(mysql.VARCHAR(255))


####################################
# Single table object tasks
# operates on a single post object
####################################

# take a single json dictionary object
# create table objects
# insert to database
def createTableObjects(jobj,session):
	author = Author(
		dataset_id = reddit_id, 
		# sqlalchemy auto-increments primary keys by default
		# author_id = 
		username   = jobj["author"] 
		)
	print(jobj["author"])
	# session - insert to server here
	session.add(author)

# general function to create tables
# name = table name
# cols = list of tuples = (name of col, type)
# def createTable(tname, cols):
# 	__tablename__ = tname

# 	for cname, ctype in cols:
# 		if ctype.__class__ == 'int':
# 			print(cname)

# 	pass

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

	# connect to server, bind metadata
	eng = connect(user, pword, db)
	metadata = s.MetaData(bind=eng)
	print(metadata)

	# uncomment to show all fields + types
	# [print(x, jobjs[8][x].__class__) for x in sorted(jobjs[8])]

	# show fields with actual example values
	# [print(x, jobjs[8][x]) for x in sorted(jobjs[8])]
	# what type is 'distinguished'? it's always null

	# start unbound session - bind in main()
	Session = s.orm.sessionmaker()
	# configure session, create session instance
	Session.configure(bind=eng)
	session = Session()

	# now ready to start inserting to database
	for jobj in jobjs:
		createTableObjects(jobj,session)
		session.commit()
	

if __name__ == "__main__":
	main()