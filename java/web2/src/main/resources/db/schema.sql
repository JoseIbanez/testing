
create table "user" (
    "id" SERIAL,
    "email" varchar(255),
    "name" varchar(255),
    primary key ("id")
);

drop table "syslog";
create table "syslog" (
    "id" SERIAL,
    "device_name" varchar(255),
    "tenant_name" varchar(255),
    "timestamp" varchar(255),
    "message" varchar(2000),
    primary key ("id")
);
