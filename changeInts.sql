ALTER TABLE `iac`.`posts` 
CHANGE COLUMN `post_id` `post_id` INT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT '' ,
CHANGE COLUMN `parent_post_id` `parent_post_id` INT(20) UNSIGNED NULL DEFAULT NULL COMMENT '' ;
