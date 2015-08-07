# redditCommentDatabase
Raw JSON -> MySQL database using Python + sqlalchemy + markdown2 libraries
```
pip install sqlalchemy
pip install markdown2
```
Given MySQL login information and raw JSON Reddit comments:
- Organizes comments according to the Internet Arguments Corpus schema, storing table information for
  + Subreddit (seperate from Topic)
  + Discussion (link)
  + Author (username)
  + Basic Markup
  + Text
  + Post

Strips Reddit's markdown from the text and creates a basic_markdown row for each instance of markdown. The goal is to eventually discover features indicating sarcasm. Given Reddit's r/sarcasm Subreddit, there should be a good amount of data to be gleaned from the 53 million comments in the 1 month dataset, or 1.7 billion in the entire Reddit comment dataset.

The schema varies slightly from the basic IAC database. You will need to add the following:

Add row to datasets for reddit (default dataset_id = 6, change this in the script)

'subreddits' table
  - dataset_id: tinyInt(3) PK
  - subreddit_id: int(20) UN PK
  - subreddit_name: varchar(255)
  - subreddit_native_id(20)

Add to 'basic_markup' table: markup_group_id: int(11)
  - useful for grouping nested quotes, lists
    
Change in 'discussions' table: native_discussion_id from int(10) -> varchar(12)
  - because reddit stores native ids as strings

