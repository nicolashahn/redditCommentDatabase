# sortRedditComments.py
# Nicolas Hahn

# after main file has been split into <4gb chunks
# sort those chunks by discussion, then timestamp
# then iterate through all of them to generate a new entire dataset
# where it's completely sorted

import json
import fileinput

numFiles = 11

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


# get the first comments of each file, turn them into jObjs
# return the files on their next lines too
def getNewComments(sortedFiles):
	newComments = []
	for i in range(len(sortedFiles)):
		if sortedFiles[i].lineno() >= fileLines[i]:
			# if we finished the file, remove it
			sortedFiles.pop(i,None)
		newComments.append(jsonLineToDict(sortedFile.readline()))
	newComments = sorted(newComments, key=lambda k: (k['link_id'], k['created_utc']))
	return newComments, sortedFiles


def main():

	# for each already-split file
	# load all the comments
	# sort them
	# write them back to file
	fileLines = {}
	for i in range(numFiles):
		with open("splitData/2015_1_redditComments-"+str(i), 'r') as splitFile:
			jObjs = []
			print('sorting file '+str(i))
			for line in splitFile:
				jObjs.append(jsonLineToDict(line))
			fileLines[i] = len(jObjs)
			with open("splitData/2015_1_redditCommentsSorted-"+str(i),'w') as outFile:
				# sorts first by link_id(discussion), then the datetime posted - older first
				sorted(jObjs, key=lambda k: (k['link_id'], k['created_utc']))
				for jObj in jObjs:
					outFile.write(str(jObj)+'\n')

	# now all split files have been sorted correctly
	sortedFiles = {}
	for i in range(numFiles):
		sortedFile[i] = fileinput.FileInput("splitData/2015_1_redditCommentsSorted-"+str(i))

	# mergesort-ish
	# TODO: optimize, runs stupid slow
	with open('RC_2015-01_sorted','w') as outFile:
		lines = 0
		currComments = []
		currComments, sortedFiles = getNewComments(sortedFiles)
		while len(sortedFiles) > 0:
			newComments, sortedFiles = getNewComments(sortedFiles)
			# write currComments to file until a newComment is ranked higher
			while currComments[0]['link_id'] <= newComments[0]['link_id']:
				topComment = currComments.pop(0)
				outFile.write(str(topComment))
				lines += 1
				if lines%10000 == 0:
					print(lines,'lines written')
			currComments += newComments
			currComments = sorted(currComments, key=lambda k: (k['link_id'], k['created_utc']))

if __name__ == '__main__':
	main()