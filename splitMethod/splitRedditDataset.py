# splitRedditDataset.py
# Nicolas Hahn
# split the ~31gb Reddit 1 month dataset into manageable
# chunks - 500,000 comments each

import fileinput

inputFile = 'RC_2015-01'
linesPerFile = 5000000

i = 0
with open("splitData/2015_1_redditComments-0",'w') as fout:
	for line in fileinput.FileInput(inputFile):
		fout.write(line)
		i+=1
		if i % linesPerFile == 0:
			fout.close()
			fout = open("splitData/2015_1_redditComments-%d"%(i/linesPerFile),'w')
	fout.close()