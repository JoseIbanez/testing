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


