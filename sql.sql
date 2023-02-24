/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - career_recommendation_system
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`career_recommendation_system` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `career_recommendation_system`;

/*Table structure for table `career_expert` */

DROP TABLE IF EXISTS `career_expert`;

CREATE TABLE `career_expert` (
  `expert_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  `house` varchar(200) DEFAULT NULL,
  `post` varchar(200) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`expert_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `career_expert` */

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `time` varchar(200) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `r_date` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

/*Table structure for table `follower` */

DROP TABLE IF EXISTS `follower`;

CREATE TABLE `follower` (
  `follower_id` int(11) NOT NULL AUTO_INCREMENT,
  `expert_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`follower_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `follower` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `usertype` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','123','admin');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(200) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `expert_id` int(11) DEFAULT NULL,
  `rating` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

/*Table structure for table `tips` */

DROP TABLE IF EXISTS `tips`;

CREATE TABLE `tips` (
  `tips_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(200) DEFAULT NULL,
  `expert_id` int(11) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`tips_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tips` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(200) DEFAULT NULL,
  `uemail` varchar(200) DEFAULT NULL,
  `uphone` bigint(20) DEFAULT NULL,
  `uhouse` varchar(200) DEFAULT NULL,
  `upost` varchar(200) DEFAULT NULL,
  `upin` int(11) DEFAULT NULL,
  `uimage` varchar(200) DEFAULT NULL,
  `ugender` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

/*Table structure for table `vaccancy` */

DROP TABLE IF EXISTS `vaccancy`;

CREATE TABLE `vaccancy` (
  `vaccancy_id` int(11) NOT NULL AUTO_INCREMENT,
  `expert_id` int(11) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `company_name` varchar(200) DEFAULT NULL,
  `post` varchar(200) DEFAULT NULL,
  `no_of_vaccancy` varchar(200) DEFAULT NULL,
  `last_date` varchar(200) DEFAULT NULL,
  `qualifications` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`vaccancy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `vaccancy` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
