import findspark
findspark.init()

from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("ParquetExample").getOrCreate()

df = spark.read.parquet(
    "./yellow_tripdata_2020-02.parquet")
df.printSchema()



from pyspark.sql.functions import col
updated_df = df.withColumn(
    "PULocationID", col("PULocationID").cast("int"))


from pyspark.sql.functions import days
spark.sql("CREATE DATABASE IF NOT EXISTS nyc")
updated_df.writeTo("nyc.taxis") \
    .partitionedBy(days("tpep_pickup_datetime")) \
    .createOrReplace()

