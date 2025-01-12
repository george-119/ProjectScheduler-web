/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - complete_my_project
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`complete_my_project` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `complete_my_project`;

/*Table structure for table `attandance` */

DROP TABLE IF EXISTS `attandance`;

CREATE TABLE `attandance` (
  `attandenceid` int(11) NOT NULL AUTO_INCREMENT,
  `exassignid` int(11) DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `grouplid` int(11) DEFAULT NULL,
  PRIMARY KEY (`attandenceid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `attandance` */

insert  into `attandance`(`attandenceid`,`exassignid`,`file`,`date`,`grouplid`) values 
(1,1,'/static/project/Complete my project.docx','2020-11-1',17),
(2,2,'/static/project/Complete my project.docx','2020-11-3',23);

/*Table structure for table `chat1` */

DROP TABLE IF EXISTS `chat1`;

CREATE TABLE `chat1` (
  `chatid` int(11) NOT NULL AUTO_INCREMENT,
  `formid` int(11) DEFAULT NULL,
  `toid` int(11) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `chat1` */

/*Table structure for table `ext_org` */

DROP TABLE IF EXISTS `ext_org`;

CREATE TABLE `ext_org` (
  `eoid` int(11) NOT NULL AUTO_INCREMENT,
  `orgname` varchar(100) DEFAULT NULL,
  `orgplace` varchar(50) DEFAULT NULL,
  `orgpin` bigint(20) DEFAULT NULL,
  `orgphone` bigint(20) DEFAULT NULL,
  `orgwebsite` varchar(50) DEFAULT NULL,
  `orglat` float DEFAULT NULL,
  `orglongi` float DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `loginid` int(11) DEFAULT NULL,
  PRIMARY KEY (`eoid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `ext_org` */

insert  into `ext_org`(`eoid`,`orgname`,`orgplace`,`orgpin`,`orgphone`,`orgwebsite`,`orglat`,`orglongi`,`email`,`loginid`) values 
(1,'max','calicut',695887,9875698547,'ewfwf',11.2588,75.7804,'max@gmail.com',19),
(2,'max','malapuram',987554,9856987458,'wwwww.in',4.2,8.2,'kkk@gmail.com',2),
(4,'vites','trivandrum',478995,9863201478,'pppp.in',6.6,88.2,'paul@gmail.com',26),
(5,'arieon','kakkanjeri',689557,9878888888,'arieon.in',8.2,27,'ar@gmail.com',27);

/*Table structure for table `external_assign` */

DROP TABLE IF EXISTS `external_assign`;

CREATE TABLE `external_assign` (
  `exassignid` int(11) NOT NULL AUTO_INCREMENT,
  `groupid` int(11) DEFAULT NULL,
  `eolid` int(11) DEFAULT NULL,
  PRIMARY KEY (`exassignid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `external_assign` */

insert  into `external_assign`(`exassignid`,`groupid`,`eolid`) values 
(1,2,19),
(4,23,19),
(5,28,19);

/*Table structure for table `file` */

DROP TABLE IF EXISTS `file`;

CREATE TABLE `file` (
  `fileid` int(11) NOT NULL AUTO_INCREMENT,
  `grouplid` int(11) DEFAULT NULL,
  `file` varchar(200) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`fileid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `file` */

insert  into `file`(`fileid`,`grouplid`,`file`,`date`) values 
(1,29,'/static/file/dfd _cmp_proj.pdf','2021-03-08'),
(2,4,'/static/file/dfd _cmp_proj.pdf',NULL);

/*Table structure for table `group_members` */

DROP TABLE IF EXISTS `group_members`;

CREATE TABLE `group_members` (
  `grpmemid` int(11) NOT NULL AUTO_INCREMENT,
  `groupid` int(11) DEFAULT NULL,
  `studentid` int(11) DEFAULT NULL,
  PRIMARY KEY (`grpmemid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `group_members` */

insert  into `group_members`(`grpmemid`,`groupid`,`studentid`) values 
(6,17,24),
(7,4,24),
(8,4,25);

/*Table structure for table `group_table` */

DROP TABLE IF EXISTS `group_table`;

CREATE TABLE `group_table` (
  `groupid` int(11) NOT NULL AUTO_INCREMENT,
  `projectname` varchar(100) DEFAULT NULL,
  `membercount` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  `batch` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `loginid` int(11) DEFAULT NULL,
  PRIMARY KEY (`groupid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `group_table` */

insert  into `group_table`(`groupid`,`projectname`,`membercount`,`email`,`language`,`batch`,`status`,`date`,`loginid`) values 
(2,'complete my project',6,'grp@gmail.com','python','s4','on going','2020-11-13',4),
(3,'new project',8,'aaaa@gmail.com','java','s5','on going','2021-06-25',23),
(4,'qwerty',5,'ar@gmail.com','python','s5','on going','2020-12-04',28),
(5,'new',8,'eeeee','python','s1','on going','2020-12-03',29);

/*Table structure for table `internal_assign` */

DROP TABLE IF EXISTS `internal_assign`;

CREATE TABLE `internal_assign` (
  `inassignid` int(11) NOT NULL AUTO_INCREMENT,
  `igid` int(11) DEFAULT NULL,
  `groupid` int(11) DEFAULT NULL,
  PRIMARY KEY (`inassignid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

/*Data for the table `internal_assign` */

insert  into `internal_assign`(`inassignid`,`igid`,`groupid`) values 
(1,0,0),
(16,3,4),
(17,3,4),
(18,2,17),
(19,2,28),
(20,2,29),
(21,3,29);

/*Table structure for table `internal_guide` */

DROP TABLE IF EXISTS `internal_guide`;

CREATE TABLE `internal_guide` (
  `igid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `pin` bigint(20) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `loginid` int(11) DEFAULT NULL,
  PRIMARY KEY (`igid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `internal_guide` */

insert  into `internal_guide`(`igid`,`name`,`email`,`phone`,`gender`,`place`,`pin`,`image`,`loginid`) values 
(2,'Paulson Mathew','paul@gmail.com',7902347726,'male','calicut',673008,'/static/internal_guide/Screenshot (73).png',2),
(3,'geo','geo@gmail.com',3545567987,'male','adivaram',123211,'/static/internal_guide/Screenshot (64).png',4);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'max','1234','external'),
(3,'intern','12345','internal'),
(4,'group','123456','group');

/*Table structure for table `progress` */

DROP TABLE IF EXISTS `progress`;

CREATE TABLE `progress` (
  `progressid` int(11) NOT NULL AUTO_INCREMENT,
  `grouplid` int(11) DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  `percentage` varchar(100) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`progressid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `progress` */

insert  into `progress`(`progressid`,`grouplid`,`file`,`percentage`,`date`) values 
(1,23,'hhhhh','75','10-5-2000'),
(2,NULL,'/static/user/2021_05_31_12_42_23.313448.jpg','85',NULL),
(3,NULL,'/static/user/2021_05_31_12_42_25.296936.jpg','85',NULL),
(4,NULL,'/static/user/2021_05_31_12_48_03.094984.jpg','50','2021-05-31'),
(5,4,'/static/user/2021_05_31_12_55_21.789597.jpg','90','2021-05-31');

/*Table structure for table `project_schedule` */

DROP TABLE IF EXISTS `project_schedule`;

CREATE TABLE `project_schedule` (
  `pschid` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) DEFAULT NULL,
  `batch` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pschid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `project_schedule` */

insert  into `project_schedule`(`pschid`,`file`,`batch`) values 
(1,'/static/project/Complete my project.docx','s5'),
(3,'/static/project/Photo.jpeg','s4'),
(4,'/static/schedule/Complete my project.docx','s5');

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `studentid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `pin` bigint(20) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `pic` varchar(100) DEFAULT NULL,
  `batch` varchar(50) DEFAULT NULL,
  `loginid` int(11) DEFAULT NULL,
  PRIMARY KEY (`studentid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`studentid`,`name`,`place`,`pin`,`phone`,`gender`,`email`,`pic`,`batch`,`loginid`) values 
(7,'maneesha','calicut',673008,5555555555,'female','mani@gmail.com','/static/student/Screenshot (85).png','s4',24),
(8,'vyshnavi','naduvnnur',673008,3256598745,'female','ssssss@gmail.com','/static/student/Screenshot (84).png','s4',25);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
