from pyspark.sql import SparkSession

spark: SparkSession = (
    SparkSession.builder.appName("simple analysis").master("local[*]").getOrCreate()
)

schema = StructType(
    [
        StructField("flight_number", StringType()),
        StructField("aircraft_type", StringType()),
        StructField("bearing", FloatType()),
        StructField(
            "location",
            StructType(
                [
                    StructField("longitude", FloatType()),
                    StructField("latitude", FloatType()),
                ]
            ),
        ),
        StructField("elevation", FloatType()),
        StructField("ground_speed", FloatType()),
        StructField("timestamp", TimestampType()),
    ]
)

df = spark.read.schema(schema).parquet("data/flight_events/")
rdd = df.rdd

print(rdd.count())
(rdd.count()).write.mode("overwrite").parquet("data/number_of_flights")