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

# remove fk constraints to change post_id from mediumint -> int
alter table quotes drop foreign key post_id;
alter table post_stances drop foreign key post_id;
alter table mturk_2010_qr_entries drop foreign key post_id;
alter table mturk_2010_p123_posts drop foreign key post_id;


# embiggen number of posts the db can hold
ALTER TABLE `iac`.`posts` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ,
CHANGE COLUMN `parent_post_id` `parent_post_id` INT(20) UNSIGNED NULL DEFAULT NULL COMMENT '' ;
*/

/*

# looks like composite foreign key - how to deal with?
CREATE TABLE `quotes` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `quote_index` smallint(5) unsigned NOT NULL DEFAULT '0',
  `parent_quote_index` smallint(5) unsigned DEFAULT NULL,
  `text_index` int(10) unsigned DEFAULT NULL,
  `text_id` int(10) unsigned DEFAULT NULL,
  `source_discussion_id` mediumint(8) unsigned DEFAULT NULL,
  `source_post_id` mediumint(8) unsigned DEFAULT NULL,
  `source_start` int(10) unsigned DEFAULT NULL,
  `source_end` int(10) unsigned DEFAULT NULL,
  `source_truncated` tinyint(1) DEFAULT NULL,
  `source_altered` tinyint(1) DEFAULT NULL,
  `alternative_source_info` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`post_id`,`quote_index`),
  KEY `dataset_id` (`dataset_id`,`text_id`),
  CONSTRAINT `quotes_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`),
  CONSTRAINT `quotes_ibfk_2` FOREIGN KEY (`dataset_id`, `text_id`) REFERENCES `texts` (`dataset_id`, `text_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
*/

