-- MySQL dump 10.13  Distrib 5.5.23, for Win64 (x86)
--
-- Host: localhost    Database: heroku_16092c835aedf9e
-- ------------------------------------------------------
-- Server version	5.5.23

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
-- Table structure for table `dota_db`
--

DROP TABLE IF EXISTS `dota_db`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dota_db` (
  `user_id` varchar(15) NOT NULL,
  `teams_dota` varchar(100) NOT NULL DEFAULT '0;',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dota_db`
--

LOCK TABLES `dota_db` WRITE;
/*!40000 ALTER TABLE `dota_db` DISABLE KEYS */;
INSERT INTO `dota_db` VALUES ('201501278','0;'),('414458367','0;');
/*!40000 ALTER TABLE `dota_db` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dota_matches`
--

DROP TABLE IF EXISTS `dota_matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dota_matches` (
  `team1` varchar(100) NOT NULL,
  `team2` varchar(100) NOT NULL,
  `tournament` varchar(100) NOT NULL,
  `result` varchar(100) DEFAULT NULL,
  `id` varchar(10) NOT NULL,
  `match_time` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dota_matches`
--

LOCK TABLES `dota_matches` WRITE;
/*!40000 ALTER TABLE `dota_matches` DISABLE KEYS */;
INSERT INTO `dota_matches` VALUES ('Empire','Liquid','DreamLeague Season 8',NULL,'55323','8.11,  21:30'),('Empire','Secret','DreamLeague Season 8',NULL,'55325','7.11,  19:00'),('Empire','Na’Vi','DreamLeague Season 8',NULL,'56182','6.11,  23:00'),('coL','VGJ.Storm','Captains Draft 4.0',NULL,'57367','7.11,  23:00'),('OpTic','Immortals','Captains Draft 4.0',NULL,'57368','8.11,  02:00'),('TBD','TBD','Captains Draft 4.0',NULL,'57369','8.11,  23:00'),('Empire','TBD','Captains Draft 4.0',NULL,'57399','5.11,  19:58'),('TBD','TBD','Dota PIT MINOR',NULL,'57604','5.11,  18:49'),('Vega','MoF','DreamLeague Season 8',NULL,'57607','6.11,  20:30'),('Vega','Secret','DreamLeague Season 8',NULL,'57608','7.11,  21:30'),('Virtus.Pro','MoF','DreamLeague Season 8',NULL,'57609','8.11,  00:00'),('Liquid','OG','DreamLeague Season 8',NULL,'57610','8.11,  19:00'),('Secret','MoF','DreamLeague Season 8',NULL,'57611','9.11,  00:00'),('DC','OpTic','ROG Masters 2017',NULL,'57699','6.11,  02:30'),('VG','TBD','The Summit 8',NULL,'57700','7.11,  13:00'),('LGD.cn','VGJ.Thunder','The Summit 8',NULL,'57701','7.11,  13:00'),('TBD','TBD','The Summit 8',NULL,'57702','7.11,  16:00'),('TBD','TBD','The Summit 8',NULL,'57703','8.11,  12:00'),('TBD','TBD','The Summit 8',NULL,'57704','8.11,  15:00');
/*!40000 ALTER TABLE `dota_matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dota_teams`
--

DROP TABLE IF EXISTS `dota_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dota_teams` (
  `team_name` varchar(20) NOT NULL,
  `region` varchar(7) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dota_teams`
--

LOCK TABLES `dota_teams` WRITE;
/*!40000 ALTER TABLE `dota_teams` DISABLE KEYS */;
INSERT INTO `dota_teams` VALUES ('NewBee','China',2),('LGD.cn','China',3),('Liquid','Europe',4),('OG','Europe',5),('EG','NA',6),('IG','China',7),('Virtus.Pro','CIS',8),('LGD.FY','China',9),('Secret','Europe',10),('VG','China',11),('iG.V','China',12),('Empire','CIS',13),('EHOME','China',14),('VGJ.Thunder','China',15),('TnC','Sea',16),('Mineski','Sea',17),('DC','NA',18),('Na\'Vi','CIS',19),('Fnatic','Sea',20),('Vega','CIS',21),('Clutch','Sea',22),('XctN','Sea',23),('WGU','Sea',24),('EHOME.K','China',25),('coL','NA',26),('Spirit','CIS',27),('Immortals','NA',28),('HappyFeet','Sea',29),('SFT','Europe',30),('Infamous','SA',31),('HR','Europe',32),('Mouz','Europe',33),('SGe','SA',34),('Gambit','Europe',35),('M19','CIS',36),('Effect','CIS',37),('EPG','Europe',38),('Spartak','CIS',39),('DC.SA','SA',40),('Comanche','CIS',41),('VGJ.Storm','NA',42),('KG','China',43),('DD','CIS',44),('No','CIS',45),('MidOrFeed','Europe',46),('Leviathan','NA',47),('OpTic','NA',48);
/*!40000 ALTER TABLE `dota_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'heroku_16092c835aedf9e'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-06  1:53:35
