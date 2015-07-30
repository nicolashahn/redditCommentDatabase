# Nicolas Hahn
# in: Raw JSON in text format, one object per line
# out: MySQL insertions for each object according to schema

import json
import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base



# create base table class
Base = declarative_base()


# json text dump -> list of json-dicts
def jsonDataToDict(data):
	jobjs = []
	for line in data:
		jline = json.loads(line)
		jobjs.append(jline)
		# print([x+": "+str(jline[x]) for x in sorted(jline)])
	return jobjs

# open connection to database
# then return engine object
def connect(username, password, database):
	db_uri = 'mysql://{}:{}@localhost/{}'.format(username, password, database)
	engine = s.create_engine(db_uri)
	engine.connect()
	return engine

# general function to create tables
# name = table name
# cols = list of tuples = (name of col, type)
def createTable(name, cols):

	pass

# dataset = int
# id = int
# username = varchar(30)
def insertAuthor(dataset, id, username):
	pass


def main():

	# connect to server, bind metadata
	eng = connect('root','nbhnbh','iac')
	metadata = s.MetaData(bind=eng)
	print(metadata)
	
	# raw text -> json dicts
	data = open('sampleComments','r',)
	jobjs = jsonDataToDict(data)
	( [print(x, jobjs[8][x].__class__) for x in sorted(jobjs[8])] )

	

if __name__ == "__main__":
	main()