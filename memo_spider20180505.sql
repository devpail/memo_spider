-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: memo_spider
-- ------------------------------------------------------
-- Server version	5.7.18-1

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
-- Table structure for table `bd_baike`
--

DROP TABLE IF EXISTS `bd_baike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_baike` (
  `id` varchar(36) NOT NULL,
  `singer_id` varchar(36) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `href` varchar(255) DEFAULT NULL,
  `html_doc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bd_baike_item`
--

DROP TABLE IF EXISTS `bd_baike_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_baike_item` (
  `id` varchar(36) NOT NULL,
  `baike_id` varchar(36) DEFAULT NULL,
  `order` int(3) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `value` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bd_baike_relations`
--

DROP TABLE IF EXISTS `bd_baike_relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_baike_relations` (
  `id` varchar(36) NOT NULL,
  `singer_id` varchar(36) DEFAULT NULL,
  `relations` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `baike_url` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bd_singer`
--

DROP TABLE IF EXISTS `bd_singer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_singer` (
  `id` varchar(36) NOT NULL COMMENT '歌手id',
  `name` varchar(255) NOT NULL COMMENT '歌手名称',
  `href` varchar(255) NOT NULL COMMENT '歌手详情页面链接',
  `time` varchar(20) NOT NULL COMMENT '抓取时间',
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '抓取状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bd_singer_info`
--

DROP TABLE IF EXISTS `bd_singer_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bd_singer_info` (
  `id` varchar(36) NOT NULL COMMENT 'id',
  `singer_id` varchar(36) DEFAULT NULL COMMENT '歌手表id',
  `type` varchar(100) DEFAULT NULL COMMENT '歌手类型',
  `img` varchar(255) DEFAULT NULL COMMENT '歌手头像',
  `hot` varchar(50) DEFAULT NULL COMMENT '热度',
  `count_gq` varchar(50) DEFAULT NULL COMMENT '歌曲数量',
  `count_zj` varchar(50) DEFAULT NULL COMMENT '专辑数量',
  `count_mv` varchar(50) DEFAULT NULL COMMENT 'MV数量',
  `time` varchar(20) DEFAULT NULL COMMENT '抓取时间',
  `status` int(11) DEFAULT '0' COMMENT '抓取状态',
  `introduce` text COMMENT '歌手介绍',
  `baike_url` varchar(255) DEFAULT NULL COMMENT '百度百科地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `juzi_pageurl`
--

DROP TABLE IF EXISTS `juzi_pageurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `juzi_pageurl` (
  `id` varchar(36) NOT NULL,
  `href` varchar(255) NOT NULL,
  `time` varchar(20) NOT NULL,
  `status` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `juzi_starurl`
--

DROP TABLE IF EXISTS `juzi_starurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `juzi_starurl` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `href` varchar(255) NOT NULL,
  `time` varchar(20) NOT NULL,
  `status` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-05 15:25:09
