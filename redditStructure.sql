CREATE DATABASE  IF NOT EXISTS `reddit` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `reddit`;
-- MySQL dump 10.13  Distrib 5.6.24, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: iac
-- ------------------------------------------------------
-- Server version	5.5.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authors` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned NOT NULL DEFAULT '0',
  `username` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  -- `reputation` int(16) DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`author_id`),
  CONSTRAINT `authors_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`dataset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_markup`
--

DROP TABLE IF EXISTS `basic_markup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_markup` (
  `dataset_id` tinyint(3) unsigned DEFAULT NULL,
  `text_id` int(10) unsigned DEFAULT NULL,
  `markup_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `start` int(10) unsigned DEFAULT NULL,
  `end` int(10) unsigned DEFAULT NULL,
  `type_name` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `attribute_str` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`markup_id`),
  KEY `dataset_id` (`dataset_id`,`text_id`),
  CONSTRAINT `basic_markup_ibfk_1` FOREIGN KEY (`dataset_id`, `text_id`) REFERENCES `texts` (`dataset_id`, `text_id`)
) ENGINE=InnoDB AUTO_INCREMENT=324902 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `constituencyparses`
--

DROP TABLE IF EXISTS `constituencyparses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `constituencyparses` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned NOT NULL DEFAULT '0',
  `node_index` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `sentence_index` mediumint(8) unsigned DEFAULT NULL,
  `parent_node_index` mediumint(8) unsigned DEFAULT NULL,
  `descendant_right_index` mediumint(8) unsigned DEFAULT NULL,
  `parse_tag_id` smallint(5) unsigned DEFAULT NULL,
  `token_index` mediumint(8) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`text_id`,`node_index`),
  KEY `dataset_id` (`dataset_id`,`text_id`,`sentence_index`),
  KEY `dataset_id_2` (`dataset_id`,`text_id`,`token_index`),
  KEY `parse_tag_id` (`parse_tag_id`),
  CONSTRAINT `constituencyParses_ibfk_2` FOREIGN KEY (`dataset_id`, `text_id`, `sentence_index`) REFERENCES `sentences` (`dataset_id`, `text_id`, `sentence_index`),
  CONSTRAINT `constituencyParses_ibfk_3` FOREIGN KEY (`dataset_id`, `text_id`, `token_index`) REFERENCES `tokens` (`dataset_id`, `text_id`, `token_index`),
  CONSTRAINT `constituencyParses_ibfk_4` FOREIGN KEY (`parse_tag_id`) REFERENCES `parsetags` (`parse_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convinceme_discussion_stance_votes`
--

DROP TABLE IF EXISTS `convinceme_discussion_stance_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convinceme_discussion_stance_votes` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `discussion_stance_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `votes` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`discussion_stance_id`),
  CONSTRAINT `convinceme_discussion_stance_votes_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `convinceme_discussion_stance_votes_ibfk_2` FOREIGN KEY (`dataset_id`, `discussion_id`, `discussion_stance_id`) REFERENCES `discussion_stances` (`dataset_id`, `discussion_id`, `discussion_stance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convoteauthorsextras`
--

DROP TABLE IF EXISTS `convoteauthorsextras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convoteauthorsextras` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned NOT NULL DEFAULT '0',
  `party` enum('D','R','I','X') DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`author_id`),
  CONSTRAINT `convoteAuthorsExtras_ibfk_1` FOREIGN KEY (`dataset_id`, `author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convoteconcatenatedpostsextras`
--

DROP TABLE IF EXISTS `convoteconcatenatedpostsextras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convoteconcatenatedpostsextras` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned NOT NULL DEFAULT '0',
  `raw_score` float DEFAULT NULL,
  `normalized_score` float DEFAULT NULL,
  `link_strength` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`author_id`),
  KEY `dataset_id` (`dataset_id`,`author_id`),
  CONSTRAINT `convoteConcatenatedPostsExtras_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `convoteConcatenatedPostsExtras_ibfk_2` FOREIGN KEY (`dataset_id`, `author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convotementions`
--

DROP TABLE IF EXISTS `convotementions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convotementions` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned DEFAULT NULL,
  `text_index` int(10) unsigned NOT NULL DEFAULT '0',
  `mention_author_id` int(10) unsigned DEFAULT NULL,
  `useless_digit` tinyint(3) unsigned DEFAULT NULL,
  `mention_name` char(26) DEFAULT NULL,
  `raw_score` float DEFAULT NULL,
  `normalized_score` float DEFAULT NULL,
  `link_strength` smallint(5) unsigned DEFAULT NULL,
  `high_precision_normalized_score` float DEFAULT NULL,
  `high_precision_link_strength` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`post_id`,`text_index`),
  KEY `dataset_id` (`dataset_id`,`mention_author_id`),
  CONSTRAINT `convoteMentions_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `convoteMentions_ibfk_2` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`),
  CONSTRAINT `convoteMentions_ibfk_3` FOREIGN KEY (`dataset_id`, `mention_author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convotepostsextras`
--

DROP TABLE IF EXISTS `convotepostsextras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convotepostsextras` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `stage_two` tinyint(1) DEFAULT NULL,
  `stage_three` tinyint(1) DEFAULT NULL,
  `yield_start` int(10) unsigned DEFAULT NULL,
  `bill_mentioned` tinyint(1) DEFAULT NULL,
  `filename` char(26) DEFAULT NULL,
  `source_page` smallint(5) unsigned DEFAULT NULL,
  `source_index` smallint(5) unsigned DEFAULT NULL,
  `raw_score` float DEFAULT NULL,
  `normalized_score` float DEFAULT NULL,
  `link_strength` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`post_id`),
  CONSTRAINT `convotePostsExtras_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `convotePostsExtras_ibfk_2` FOREIGN KEY (`dataset_id`, `discussion_id`, `post_id`) REFERENCES `posts` (`dataset_id`, `discussion_id`, `post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `convotevotes`
--

DROP TABLE IF EXISTS `convotevotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `convotevotes` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned NOT NULL DEFAULT '0',
  `vote` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`author_id`),
  KEY `dataset_id` (`dataset_id`,`author_id`),
  CONSTRAINT `convoteVotes_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `convoteVotes_ibfk_2` FOREIGN KEY (`dataset_id`, `author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `datasets`
--

DROP TABLE IF EXISTS `datasets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datasets` (
  `dataset_id` tinyint(3) unsigned NOT NULL,
  `name` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `source_url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `description` text COLLATE utf8mb4_bin,
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dependencies`
--

DROP TABLE IF EXISTS `dependencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dependencies` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned NOT NULL DEFAULT '0',
  `sentence_index` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `dependency_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `relation_id` smallint(5) unsigned NOT NULL,
  `governor_token_index` mediumint(8) unsigned DEFAULT NULL,
  `dependent_token_index` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`dataset_id`,`text_id`,`sentence_index`,`dependency_id`),
  KEY `relation_id` (`relation_id`),
  KEY `dataset_id` (`dataset_id`,`text_id`,`governor_token_index`),
  KEY `dataset_id_2` (`dataset_id`,`text_id`,`dependent_token_index`),
  CONSTRAINT `dependencies_ibfk_1` FOREIGN KEY (`relation_id`) REFERENCES `dependencyrelations` (`relation_id`),
  CONSTRAINT `dependencies_ibfk_2` FOREIGN KEY (`dataset_id`, `text_id`, `governor_token_index`) REFERENCES `tokens` (`dataset_id`, `text_id`, `token_index`),
  CONSTRAINT `dependencies_ibfk_3` FOREIGN KEY (`dataset_id`, `text_id`, `dependent_token_index`) REFERENCES `tokens` (`dataset_id`, `text_id`, `token_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dependencyrelations`
--

DROP TABLE IF EXISTS `dependencyrelations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dependencyrelations` (
  `relation_id` smallint(5) unsigned NOT NULL,
  `hierarchy_parent_relation_id` smallint(5) unsigned DEFAULT NULL,
  `relation` varchar(255) NOT NULL,
  `relation_long` varchar(255) NOT NULL,
  PRIMARY KEY (`relation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discussion_stances`
--

DROP TABLE IF EXISTS `discussion_stances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_stances` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `discussion_stance_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_stance` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `topic_id` mediumint(8) unsigned DEFAULT NULL,
  `topic_stance_id` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`discussion_stance_id`),
  KEY `topic_id` (`topic_id`,`topic_stance_id`),
  CONSTRAINT `discussion_stances_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `discussion_stances_ibfk_2` FOREIGN KEY (`topic_id`, `topic_stance_id`) REFERENCES `topic_stances` (`topic_id`, `topic_stance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discussions`
--

DROP TABLE IF EXISTS `discussions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussions` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `discussion_url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `topic_id` mediumint(8) unsigned DEFAULT NULL,
  `initiating_author_id` int(10) unsigned DEFAULT NULL,
  `native_discussion_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`),
  KEY `topic_id` (`topic_id`),
  KEY `dataset_id` (`dataset_id`,`initiating_author_id`),
  CONSTRAINT `discussions_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`dataset_id`),
  CONSTRAINT `discussions_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`),
  CONSTRAINT `discussions_ibfk_3` FOREIGN KEY (`dataset_id`, `initiating_author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discussionstrainingdevtest`
--

DROP TABLE IF EXISTS `discussionstrainingdevtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussionstrainingdevtest` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `task` varchar(20) NOT NULL DEFAULT '',
  `set_name` enum('training','development','test','discarded') DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`task`),
  CONSTRAINT `discussionsTrainingDevTest_ibfk_1` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mturk_author_stance`
--

DROP TABLE IF EXISTS `mturk_author_stance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mturk_author_stance` (
  `topic_id` mediumint(8) unsigned DEFAULT NULL,
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned NOT NULL DEFAULT '0',
  `topic_stance_id_1` tinyint(3) unsigned DEFAULT NULL,
  `topic_stance_votes_1` tinyint(3) unsigned DEFAULT NULL,
  `topic_stance_id_2` tinyint(3) unsigned DEFAULT NULL,
  `topic_stance_votes_2` tinyint(3) unsigned DEFAULT NULL,
  `topic_stance_votes_other` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`author_id`),
  KEY `dataset_id` (`dataset_id`,`author_id`),
  KEY `topic_id` (`topic_id`,`topic_stance_id_1`),
  KEY `topic_id_2` (`topic_id`,`topic_stance_id_2`),
  CONSTRAINT `mturk_author_stance_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`dataset_id`),
  CONSTRAINT `mturk_author_stance_ibfk_2` FOREIGN KEY (`dataset_id`, `author_id`) REFERENCES `authors` (`dataset_id`, `author_id`),
  CONSTRAINT `mturk_author_stance_ibfk_3` FOREIGN KEY (`topic_id`, `topic_stance_id_1`) REFERENCES `topic_stances` (`topic_id`, `topic_stance_id`),
  CONSTRAINT `mturk_author_stance_ibfk_4` FOREIGN KEY (`topic_id`, `topic_stance_id_2`) REFERENCES `topic_stances` (`topic_id`, `topic_stance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parent_relations`
--

DROP TABLE IF EXISTS `parent_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parent_relations` (
  `dataset_id` tinyint(3) unsigned NOT NULL,
  `parent_relation_id` tinyint(4) NOT NULL DEFAULT '0',
  `relation` varchar(60) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`parent_relation_id`),
  UNIQUE KEY `dataset_id` (`dataset_id`,`parent_relation_id`),
  CONSTRAINT `parent_relations_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`dataset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parsetags`
--

DROP TABLE IF EXISTS `parsetags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parsetags` (
  `parse_tag_id` smallint(5) unsigned NOT NULL,
  `parse_tag` varchar(255) DEFAULT NULL,
  `parse_tag_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`parse_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `post_stances`
--

DROP TABLE IF EXISTS `post_stances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `postags`
--

DROP TABLE IF EXISTS `postags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postags` (
  `pos_tag_id` smallint(5) unsigned NOT NULL,
  `pos_tag` varchar(255) DEFAULT NULL,
  `pos_tag_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pos_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `discussion_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author_id` int(10) unsigned DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `parent_post_id` mediumint(8) unsigned DEFAULT NULL,
  `parent_missing` tinyint(1) DEFAULT '0',
  `native_post_id` int(10) unsigned DEFAULT NULL,
  `text_id` int(10) unsigned DEFAULT NULL,
  `parent_relation_id` tinyint(4) DEFAULT NULL,
  `votes` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`discussion_id`,`post_id`),
  KEY `dataset_id` (`dataset_id`,`text_id`),
  KEY `dataset_id_2` (`dataset_id`,`author_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`dataset_id`, `text_id`) REFERENCES `texts` (`dataset_id`, `text_id`),
  CONSTRAINT `posts_ibfk_2` FOREIGN KEY (`dataset_id`, `discussion_id`) REFERENCES `discussions` (`dataset_id`, `discussion_id`),
  CONSTRAINT `posts_ibfk_3` FOREIGN KEY (`dataset_id`, `author_id`) REFERENCES `authors` (`dataset_id`, `author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quotes`
--

DROP TABLE IF EXISTS `quotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sentences`
--

DROP TABLE IF EXISTS `sentences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentences` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned NOT NULL DEFAULT '0',
  `sentence_index` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `start` int(10) unsigned DEFAULT NULL,
  `end` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`text_id`,`sentence_index`),
  CONSTRAINT `sentences_ibfk_1` FOREIGN KEY (`dataset_id`, `text_id`) REFERENCES `texts` (`dataset_id`, `text_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `texts`
--

DROP TABLE IF EXISTS `texts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `texts` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned NOT NULL DEFAULT '0',
  `text` longtext COLLATE utf8mb4_bin,
  PRIMARY KEY (`dataset_id`,`text_id`),
  CONSTRAINT `texts_ibfk_1` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`dataset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tokens` (
  `dataset_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `text_id` int(10) unsigned NOT NULL DEFAULT '0',
  `token_index` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `sentence_index` mediumint(8) unsigned DEFAULT NULL,
  `start` int(10) unsigned DEFAULT NULL,
  `end` int(10) unsigned DEFAULT NULL,
  `pos_tag_id` smallint(5) unsigned DEFAULT NULL,
  `word_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`text_id`,`token_index`),
  KEY `word_id` (`word_id`),
  KEY `pos_tag_id` (`pos_tag_id`),
  CONSTRAINT `tokens_ibfk_1` FOREIGN KEY (`dataset_id`, `text_id`) REFERENCES `texts` (`dataset_id`, `text_id`),
  CONSTRAINT `tokens_ibfk_2` FOREIGN KEY (`word_id`) REFERENCES `words` (`word_id`),
  CONSTRAINT `tokens_ibfk_3` FOREIGN KEY (`pos_tag_id`) REFERENCES `postags` (`pos_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topic_stances`
--

DROP TABLE IF EXISTS `topic_stances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_stances` (
  `topic_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_stance_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `stance` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`topic_id`,`topic_stance_id`),
  CONSTRAINT `topic_stances_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topics` (
  `topic_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `topic` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `word_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` text NOT NULL,
  PRIMARY KEY (`word_id`)
) ENGINE=InnoDB AUTO_INCREMENT=115415 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-31 16:11:33
