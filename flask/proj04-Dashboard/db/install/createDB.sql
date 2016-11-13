#
# Create DB
#
DROP DATABASE IF EXISTS `bdb`;
CREATE DATABASE `bdb`;

USE  `bdb`;
#
# Create Users
#

GRANT USAGE ON *.* TO 'kpi'@'localhost' IDENTIFIED BY '{{BDB_MYSQL_PASSWD}}';
GRANT USAGE ON *.* TO 'kpi'@'%'         IDENTIFIED BY '{{BDB_MYSQL_PASSWD}}';
DROP USER 'kpi'@'localhost';
DROP USER 'kpi'@'%';

CREATE USER 'kpi'@'localhost' IDENTIFIED BY '{{BDB_MYSQL_PASSWD}}';
CREATE USER 'kpi'@'%'         IDENTIFIED BY '{{BDB_MYSQL_PASSWD}}';


GRANT ALL PRIVILEGES ON bdb.* TO 'kpi'@'localhost';
GRANT ALL PRIVILEGES ON bdb.* TO 'kpi'@'%' ;

FLUSH PRIVILEGES;


#
# Table kpi
#

CREATE TABLE kpi (
  cust   varchar(20),
  kpi    varchar(20),
  domain varchar(200),
  value  integer,
  date   datetime,
  id     int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  UNIQUE KEY `kpiid` (`cust`,`kpi`,`domain`)
);


#
# Table log
#

CREATE TABLE log (
  cust varchar(20),
  kpi varchar(20),
  domain varchar(200),
  value integer,
  date datetime
);
