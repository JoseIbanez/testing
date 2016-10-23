#
# Create DB
#



#
# Create Users
#



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

CREATE USER 'kpi'@'localhost' IDENTIFIED BY 'VFhcs123!';
CREATE USER 'kpi'@'%'         IDENTIFIED BY 'VFhcs123!';


GRANT ALL PRIVILEGES ON fruit.* TO 'kpi'@'localhost';
GRANT ALL PRIVILEGES ON fruit.* TO 'kpi'@'%' ;

FLUSH PRIVILEGES;
