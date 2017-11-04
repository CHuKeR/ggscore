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
  `teams_dota` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dota_db`
--

LOCK TABLES `dota_db` WRITE;
/*!40000 ALTER TABLE `dota_db` DISABLE KEYS */;
INSERT INTO `dota_db` VALUES ('201501278','0;');
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
INSERT INTO `dota_matches` VALUES ('TBD','WGU','Captains Draft 4.0',NULL,'57361','4.11,  07:00'),('TBD','TBD','Captains Draft 4.0',NULL,'57363','3.11,  13:30'),('TBD','TBD','Captains Draft 4.0',NULL,'57364','4.11,  10:00'),('Empire','TBD','Captains Draft 4.0',NULL,'57394','4.11,  17:00'),('M19','Effect','Captains Draft 4.0',NULL,'57395','3.11,  17:00'),('Gambit','TBD','Captains Draft 4.0',NULL,'57396','3.11,  20:00'),('TBD','TBD','Captains Draft 4.0',NULL,'57397','4.11,  20:00'),('VG','OG','Dota PIT MINOR',NULL,'57593','3.11,  14:00'),('Virtus.Pro','Fnatic','Dota PIT MINOR',NULL,'57594','3.11,  17:15'),('TBD','TBD','Dota PIT MINOR',NULL,'57596','3.11,  20:30'),('Liquid','TBD','Dota PIT MINOR',NULL,'57597','4.11,  21:30'),('SGe','TBD','Dota PIT MINOR',NULL,'57598','4.11,  15:30'),('TBD','TBD','Dota PIT MINOR',NULL,'57599','4.11,  14:00'),('TBD','TBD','Dota PIT MINOR',NULL,'57600','4.11,  17:00'),('NewBee','TBD','Dota PIT MINOR',NULL,'57601','4.11,  18:30'),('TBD','TBD','Dota PIT MINOR',NULL,'57602','4.11,  20:00'),('TBD','TBD','Dota2 Professional League Season 4',NULL,'57651','3.11,  16:00'),('TBD','TBD','Dota2 Professional League Season 4',NULL,'57653','3.11,  07:00'),('TBD','TBD','Dota2 Professional League Season 4',NULL,'57654','3.11,  10:00'),('DC','VGJ.Storm','ROG Masters 2017',NULL,'57697','3.11,  21:00'),('OpTic','Leviathan','ROG Masters 2017',NULL,'57698','4.11,  00:00');
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

-- Dump completed on 2017-11-04 17:26:51
