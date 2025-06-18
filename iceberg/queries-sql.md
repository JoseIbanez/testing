
# 
docker exec -it spark-iceberg spark-sql


CREATE TABLE demo.nyc.taxis
(
  vendor_id bigint,
  trip_id bigint,
  trip_distance float,
  fare_amount double,
  store_and_fwd_flag string
)
PARTITIONED BY (vendor_id);


SELECT * 
FROM csv.`/home/iceberg/warehouse/geo.csv` 
OPTIONS (
    header true
)
limit 10;



DROP VIEW geo;

href: https://github.com/databricks/spark-csv

CREATE TEMPORARY VIEW geo
USING csv 
OPTIONS (
  path '/home/iceberg/warehouse/geo.csv',
  header true,
  inferSchema "true"
 );


SET hive.cli.print.header=true;

SELECT * FROM geo LIMIT 10;

show namespaces;
show views in nyc;
show tables in nyc;

SELECT * 
FROM parquet.`/home/iceberg/warehouse/yellow_tripdata_2009-02.parquet`
limit 10;

SELECT count(*) 
FROM parquet.`/home/iceberg/warehouse/yellow_tripdata_2009-02.parquet` ;


CREATE TEMPORARY VIEW w_trip2020
USING parquet
OPTIONS (
  path '/home/iceberg/warehouse/yellow_tripdata_2020-02.parquet'
);




CREATE TABLE demo.nyc.mygeo
(
 anzsic06 string,
 Area string,
 year bigint,
 geo_count bigint,
 ec_count bigint
)
PARTITIONED BY (year);

INSERT into demo.nyc.mygeo
Select * from geo limit 10;

drop table demo.nyc.trip2020 ;

create table demo.nyc.trip2020 
(
   VendorId bigint,
   tpep_pickup_datetime timestamp_ntz,
   tpep_dropoff_datetime timestamp_ntz,  
   tip_amount float   
)
PARTITIONED BY (VendorId);

insert into demo.nyc.trip2020
select VendorID, tpep_pickup_datetime, tpep_pickup_datetime, tip_amount 
from w_trip2020 limit 10;


# pyspark 
docker exec -it spark-iceberg pyspark

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").appName("ParquetExample").getOrCreate()


spark.read.parquet("/home/iceberg/warehouse/yellow_tripdata_2020-02.parquet").printSchema()

spark.read.parquet("/home/iceberg/warehouse/yellow_tripdata_2009-02.parquet").printSchema()

spark.read.parquet("/home/iceberg/warehouse/yellow_tripdata_2009-02.parquet").head()



docker exec -it spark-iceberg spark-sql

drop table nyc.trip2009_1;
create table demo.nyc.trip2009_1
(
  vendor_name string,
  Trip_Pickup_DateTime timestamp,
  Trip_Dropoff_DateTime timestamp,
  Passenger_Count long,
  Trip_Distance double,
  Payment_Type string,
  Total_Amt double
)
PARTITIONED BY (day(Trip_Pickup_DateTime));


CREATE TEMPORARY VIEW w_trip2009
USING parquet
OPTIONS (
  path '/home/iceberg/warehouse/yellow_tripdata_2009-02.parquet'
);


insert into demo.nyc.trip2009_1
select
  vendor_name,
  timestamp(Trip_Pickup_DateTime),
  timestamp(Trip_Dropoff_DateTime),
  Passenger_Count,
  Trip_Distance,
  Payment_Type,
  Total_Amt double
from w_trip2009 limit 10;


create table demo.nyc.metric 
(
   customer string,
   eventTime timestamp,
   source_id string,
   source_labels map<string,string>,
   metric_name string,
   metric_value double,
   metric_labels map<string,string>
)
PARTITIONED BY (day(eventTime));

INSERT INTO demo.nyc.metric
VALUES 
("BASF",   timestamp("2009-02-20 23:37:05"), "src01", map( "l1","a", "l2","d1"), 'cpu', 80.1, map("l7","ff", "l4","ggg") ),
("Denuvo", timestamp("2009-02-20 23:37:05"), "src02", map( "l1","b", "l2","d2"), 'cpu', 88.1, map("l9","ff", "l4","ggg", "l22","fi") ) 
;


select * from nyc.metric where metric_labels['l3']="ff";
