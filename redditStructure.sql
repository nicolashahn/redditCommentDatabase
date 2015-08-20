insert into datasets (dataset_id = 6,name = 'reddit', source_url = 'http://www.reddit.com', description = 'link and image board');

create table subdreddits (
					dataset_id tinyint(3),
                    subreddit_id int(20) unsigned,
                    subreddit_name varchar(255),
                    subreddit_native_id varchar(20)
                    );

set sql_mode = 'STRICT_ALL_TABLES';
alter table discussions change native_discussion_id native_discussion_id varchar(12);

alter table posts change native_post_id native_post_id varchar(12);

alter table discussions add subreddit_id int(10);

alter table basic_markup add markup_group_id int(11);
 
# select * from subreddits;