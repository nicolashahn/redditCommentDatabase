# redditCommentDatabase

For use on dataset you can find here:
https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/

Raw JSON -> MySQL database using Python + sqlalchemy + snudown libraries
- You can get sqlalchemy from pip (pip install sqlalchemy)
- snudown you need to download from github and install using setup.py (python setup.py install)

entireDatasetToMySQL.py:
- Organizes comments according to the Internet Arguments Corpus schema, storing table information for
  + Subreddit (seperate from Topic)
  + Discussion (link)
  + Author (username)
  + Basic Markup
  + Text
  + Post
- Strips Reddit's markdown from the text and creates a basic_markdown row for each instance of markdown. The goal is to eventually discover features indicating sarcasm. Given Reddit's r/sarcasm Subreddit, there should be a good amount of data to be gleaned from the 53 million comments in the 1 month dataset, or 1.7 billion in the entire Reddit comment dataset.

Usage:
```
python3 entireDatasetToMySQL.py [username] [password] [host/database] [data file]
```

The schema varies slightly from the basic IAC database. The SQL script redditStructure will update the IAC schema to work with Reddit data.

