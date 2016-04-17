
apt-get install -y python-mysql.connector

DROP TABLE hDateDevices;
CREATE TABLE hDateDevices  (
  date  DATE,
  total int,
  dc1   int,
  dc2   int
);

DROP TABLE hDateExternalCalls;
CREATE TABLE hDateExternalCalls  (
  date    DATE,
  cube1   int,
  cube2   int,
  sbc     int
);



insert into hDateDevices values ('2015-10-11',1,1);
insert into hDateDevices values ('2015-10-12',1,2);
insert into hDateDevices values ('2015-10-13',3,3);
