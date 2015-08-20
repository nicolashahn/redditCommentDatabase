# insert into datasets (dataset_id = 6,name = 'reddit', source_url = 'http://www.reddit.com',' description = 'link and image board');

# select * from discussions;

# set sql_mode = 'STRICT_ALL_TABLES';
# alter table discussions change native_discussion_id native_discussion_id varchar(12);

# alter table posts change native_post_id native_post_id varchar(12);

# alter table discussions add subreddit_id int(10);

# select * from texts where dataset_id = 6;

 # select * from posts where dataset_id = 6 and post_id > 140350;
 
 select * from subreddits where subreddit_name = 'notsarcastic';