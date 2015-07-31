# Nicolas Hahn
# in: Raw Reddit JSON post objects in text format, one object per line
# out: MySQL insertions for each object according to schema

import json
import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql


###################################
# Global variables
###################################

# create base table class
Base = declarative_base()

# start unbound session - bind in main()
Session = s.orm.sessionmaker()

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
# MySQL setup helper functions
###################################

# open connection to database
# then return engine object
def connect(username, password, database):
	db_uri = 'mysql://{}:{}@localhost/{}'.format(username, password, database)
	engine = s.create_engine(db_uri)
	engine.connect()
	return engine

# dataset = tinyint(3)
# id = integer(20)
# username = varchar(255)
def createAuthor(dataset, id, username):

	pass


####################################
# Table Classes
####################################

class Author(Base):
	__tablename__ = 'authors'

	dataset_id = s.Column(mysql.TINYINT(3), primary_key=True)
	author_id = s.Column(mysql.INTEGER(20), primary_key=True)
	username = s.Column(mysql.VARCHAR(255))


####################################
# Table Tasks
####################################

# take a single json dictionary object
# create table objects
# insert to database
def createTableObjects(jobj,session):
	author = Author(
		dataset_id = reddit_id, 
		# sqlalchemy auto-increments primary keys by default
		# author_id  = jobj[""]
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
	
	# raw text -> json dicts
	data = open('sampleComments','r',)
	jobjs = jsonDataToDict(data)

	# connect to server, bind metadata
	eng = connect('root','nbhnbh','reddit')
	metadata = s.MetaData(bind=eng)
	print(metadata)

	# uncomment to show all fields + types
	# [print(x, jobjs[8][x].__class__) for x in sorted(jobjs[8])]
	
	# show fields with actual values
	# [print(x, jobjs[8][x]) for x in sorted(jobjs[8])]
	# what type is 'distinguished'? it's always null

	# configure session, create session instance
	Session.configure(bind=eng)
	session = Session()

	# now ready to start pushing to database
	for jobj in jobjs:
		createTableObjects(jobj,session)
		session.commit()
	

if __name__ == "__main__":
	main()