from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, TimestampNTZType, MapType

schema = StructType([
    StructField("_source",StructType([
        StructField("customer",StringType()),
        StructField("eventId",StringType()),
        StructField("eventTime",TimestampType()),
        StructField("timeReceived",TimestampType()),        
        StructField("domain",StringType()),
        StructField("source",StructType([
            StructField("id",StringType()),
            StructField("labels",MapType(StringType(),StringType()))
            ])),
        StructField("metric",StructType([
            StructField("name",StringType()),
            StructField("value",DoubleType()),
            StructField("labels",MapType(StringType(),StringType()))
            ]))
        ]))
    ])

df2 = spark.read.schema(schema).json("/home/iceberg/warehouse/esm-mpn-logstash-aws-data-aggregator_data.jsonl.gz")
#df2.printSchema()
df3 = df2.select(df2._source.customer.alias("customer"), 
           df2._source.eventTime.alias("eventId"),
           df2._source.eventTime.alias("eventTime"),           
           df2._source.eventTime.alias("timeReceived"),
           df2._source.source.id.alias("source_id"),
           df2._source.source.labels.alias("source_labels"),
           df2._source.metric["name"].alias("metric_name"),
           df2._source.metric.value.alias("metric_value"),
           df2._source.metric.labels.alias("metric_labels")
          )


df3.count()
df3.head()
#df3.write.option("maxRecordsPerFile", 500000000).saveAsTable("nyc.esm_metric_06")

df3.coalesce(1).write.save("/tmp/nyc.esm_metric_09")