import json

data = open("RC_2015-01","r")

out = open("sampleComments100k","w")

i = 0
for line in data:
	if i == 100000:
		break
	out.write(line)
	i+=1
	# print(json.loads(line)["body"])