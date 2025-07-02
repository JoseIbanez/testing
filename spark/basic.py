from pyspark.sql import SparkSession


#spark = SparkSession.builder.appName("Jupyter").getOrCreate()

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

spark

spark.sql(sqlQuery="SELECT * FROM range(10) where id > 7;").show()
spark.sql("SELECT eventTime,metric_value,source_id FROM nyc.meraki_31_latency LIMIT 10").show()