/*
# scrub the database of any reddit material
# be careful
use iac;
delete from subreddits where dataset_id = 6;
delete from authors where dataset_id = 6;
delete from posts where dataset_id = 6;
delete from texts where dataset_id = 6;
delete from basic_markup where dataset_id = 6;
delete from texts where dataset_id = 6;
*/

# select * from discussions;

# set sql_mode = 'STRICT_ALL_TABLES';
# alter table discussions change native_discussion_id native_discussion_id varchar(12);

# alter table discussions add subreddit_id int(10);

# select * from discussions;