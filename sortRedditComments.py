# sortRedditComments.py
# Nicolas Hahn

# after main file has been split into <4gb chunks
# sort those chunks by discussion, then timestamp
# then iterate through all of them to generate a new entire dataset
# where it's completely sorted

import json
import fileinput
import entireDatasetToMySQL as d2m

numFiles = 11

# get the first comments of each file, turn them into jObjs
# return the files on their next lines too
def getNewComments(sortedFiles):
	newComments = []
	for i in range(len(sortedFiles)):
		if sortedFiles[i].lineno() >= fileLines[i]:
			# if we finished the file, remove it
			sortedFiles.pop(i,None)
		newComments.append(d2m.jsonLineToDict(sortedFile.readline()))
	newComments = sorted(newComments, key=lambda k: (k['link_id'], k['created_utc']))
	return newComments, sortedFiles


def main():
	fileLines = {}
	for i in range(numFiles):
		with open("splitData/2015_1_redditComments-"+int(i), 'r') as splitFile:
			jObjs = []
			print('sorting file '+str(i))
			for line in splitFile:
				jObjs.append(d2m.jsonLineToDict(line))
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

	# mergesort it
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
			currComments += newComments
			currComments = sorted(currComments, key=lambda k: (k['link_id'], k['created_utc']))
