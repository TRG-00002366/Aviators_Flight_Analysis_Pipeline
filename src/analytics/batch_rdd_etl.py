from pyspark.sql import SparkSession

spark: SparkSession = (
    SparkSession.builder.appName("simple analysis").master("local[*]").getOrCreate()
)

df = spark.read.parquet("data/flight_events/")
rdd = df.rdd

print(rdd.count())
(rdd.count()).write.mode("overwrite").parquet("data/number_of_flights")