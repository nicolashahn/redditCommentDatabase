/*
insert into datasets values(6, 'reddit', 'http://www.reddit.com', 'link and image board');

create table subreddits (
					dataset_id tinyint(3),
                    subreddit_id int(20) unsigned,
                    subreddit_name varchar(255),
                    subreddit_native_id varchar(20),
                    primary key(dataset_id, subreddit_id) 
                    );

set sql_mode = 'STRICT_ALL_TABLES';
alter table discussions change native_discussion_id native_discussion_id varchar(12);

alter table posts change native_post_id native_post_id varchar(12);

alter table discussions add subreddit_id int(10);

alter table basic_markup add markup_group_id int(11);
*/

ALTER TABLE `iac`.`posts` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ,
CHANGE COLUMN `parent_post_id` `parent_post_id` INT(20) UNSIGNED NULL DEFAULT NULL COMMENT '' ;