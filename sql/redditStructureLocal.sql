/*
# initial setup of db for reddit
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

# remove fk constraints to change post_id from mediumint -> int
alter table quotes drop foreign key quotes_ibfk_3;
# alter table post_stances drop primary key, add primary key(`dataset_id`, `discussion_id`);
alter table convotepostsextras drop foreign key convotePostsExtras_ibfk_2;
alter table convotementions drop foreign key convoteMentions_ibfk_2;
# alter table mturk_2010_qr_entries drop foreign key mturk_2010_qr_entries_ibfk_1;
# alter table mturk_2010_qr_entries drop foreign key mturk_2010_qr_entries_ibfk_2;
# alter table mturk_2010_p123_posts drop foreign key mturk_2010_p123_posts_ibfk_1;


# embiggen number of posts the db can hold
ALTER TABLE `iac`.`posts` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ,
CHANGE COLUMN `parent_post_id` `parent_post_id` INT(20) UNSIGNED NULL DEFAULT NULL COMMENT '' ;

# change fk tables as well
ALTER TABLE `iac`.`quotes` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
ALTER TABLE `iac`.`post_stances` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
ALTER TABLE `iac`.`convotepostsextras` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
ALTER TABLE `iac`.`convotementions` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
/*
ALTER TABLE `iac`.`mturk_2010_qr_entries` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
ALTER TABLE `iac`.`mturk_2010_p123_posts` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ;
*/
# add the foreign constraints back in
alter table quotes add foreign key `quotes_ibfk_3` (`dataset_id`,`discussion_id`,`post_id`) references `posts` (`dataset_id`, `discussion_id`, `post_id`);
# alter table post_stances drop primary key, add primary key(`dataset_id`, `discussion_id`,`post_id`);
alter table convotepostsextras add foreign key `convotePostsExtras_ibfk_2` (`dataset_id`,`discussion_id`,`post_id`) references `posts` (`dataset_id`, `discussion_id`, `post_id`);
alter table convotementions add foreign key `convoteMentions_ibfk_2` (`dataset_id`,`discussion_id`,`post_id`) references `posts` (`dataset_id`, `discussion_id`, `post_id`);

# alter table mturk_2010_qr_entries add foreign key `mturk_2010_qr_entries_ibfk_1` (`dataset_id`,`discussion_id`,`post_id`) references `posts` (`dataset_id`, `discussion_id`, `post_id`);
# alter table mturk_2010_qr_entries add foreign key `mturk_2010_qr_entries_ibfk_2` (`dataset_id`,`discussion_id`,`post_id`,`quote_index`) references `quotes` (`dataset_id`, `discussion_id`, `post_id`, `quote_index`);
# alter table mturk_2010_p123_posts add foreign key `mturk_2010_p123_posts_ibfk_1` (`dataset_id`,`discussion_id`,`post_id`) references `posts` (`dataset_id`, `discussion_id`, `post_id`);

/*
# the original create table commands for tables affected by above post_id change
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

CREATE TABLE `post_stances` (
   `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
   `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
   `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
   `discussion_stance_id` tinyint(3) unsigned DEFAULT NULL,
   `topic_id` mediumint(8) unsigned DEFAULT NULL,
   `topic_stance_id` tinyint(3) unsigned DEFAULT NULL,
   PRIMARY KEY (`dataset_id`,`discussion_id`,`post_id`),
   KEY `topic_id` (`topic_id`,`topic_stance_id`),
   KEY `dataset_id` (`dataset_id`,`discussion_id`,`discussion_stance_id`),
   CONSTRAINT `post_stances_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`),
   CONSTRAINT `post_stances_ibfk_2` FOREIGN KEY (`topic_id`, `topic_stance_id`) REFERENCES `topic_stances` (`topic_id`, `topic_stance_id`),
   CONSTRAINT `post_stances_ibfk_3` FOREIGN KEY (`dataset_id`, `discussion_id`, `discussion_stance_id`) REFERENCES `discussion_stances` (`dataset_id`, `discussion_id`, `discussion_stance_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin

CREATE TABLE `mturk_2010_qr_entries` (
   `page_id` smallint(5) unsigned NOT NULL DEFAULT '0',
   `tab_number` tinyint(3) unsigned NOT NULL DEFAULT '0',
   `dataset_id` tinyint(3) unsigned DEFAULT NULL,
   `discussion_id` mediumint(8) unsigned DEFAULT NULL,
   `post_id` mediumint(8) unsigned DEFAULT NULL,
   `quote_index` smallint(5) unsigned DEFAULT NULL,
   `response_text_end` int(10) unsigned DEFAULT NULL,
   `presented_quote` text COLLATE utf8mb4_bin,
   `presented_response` text COLLATE utf8mb4_bin,
   `term` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
   `topic` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
   PRIMARY KEY (`page_id`,`tab_number`),
   KEY `dataset_id` (`dataset_id`,`discussion_id`,`post_id`,`quote_index`),
   CONSTRAINT `mturk_2010_qr_entries_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`),
   CONSTRAINT `mturk_2010_qr_entries_ibfk_2` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`, `quote_index`) REFERENCES `quotes` (`dataset_id`, `discussion_id`, `post_id`, `quote_index`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin

CREATE TABLE `mturk_2010_p123_posts` (
   `p123_triple_id` smallint(5) unsigned NOT NULL DEFAULT '0',
   `triple_index` tinyint(3) unsigned NOT NULL DEFAULT '0',
   `dataset_id` tinyint(3) unsigned DEFAULT NULL,
   `discussion_id` mediumint(8) unsigned DEFAULT NULL,
   `post_id` mediumint(8) unsigned DEFAULT NULL,
   `presented_text` text COLLATE utf8mb4_bin,
   `presented_text_term_removed` text COLLATE utf8mb4_bin,
   `term` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
   `topic` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
   PRIMARY KEY (`p123_triple_id`,`triple_index`),
   KEY `dataset_id` (`dataset_id`,`discussion_id`,`post_id`),
   CONSTRAINT `mturk_2010_p123_posts_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin

*/

