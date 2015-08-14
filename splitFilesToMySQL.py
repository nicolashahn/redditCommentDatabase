# splitFilesToMySQL.py
# Nicolas Hahn
# run JSONtoMySQL.py on all split files in dataset
# will take a long time to run (about a day)

import sys
import JSONtoMySQL as j2m

def main():
	if len(sys.argv) != 6:
		print("Incorrect number of arguments given")
		print("Usage: python splitFilesToMySQL [username] [password] [host/database name] [JSON data file PREFIX] [index of last data file]")
		print("Example: python splitFilesToMySQL root password localhost/iac splitData 107")
		print("This will process all files in splitData-0, splitData-1,... to splitData-107")
		sys.exit(1)

	user = sys.argv[1]
	pword = sys.argv[2]
	db = sys.argv[3]
	prefix = sys.argv[4]
	lastIndex = sys.argv[5]

	for i in range(int(lastIndex)):
		dataFile = prefix+"-"+str(i)
		print("Starting on file",dataFile)
		j2m.main(user, pword, db, dataFile)
		print(dataFile,"completed.")

if __name__ == "__main__":
	main()
