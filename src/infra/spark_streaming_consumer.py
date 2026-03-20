from pyspark.sql import SparkSession
from pyspark.sql.types import (FloatType, StringType, StructField, StructType,
                               TimestampType)
from pyspark.sql.functions import from_json

spark = (
    SparkSession.builder.appName("spark_streaming_consumer")
    .master("local[*]")
    .config("--packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1")
    .getOrCreate()
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
# Read from Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "flight_events")
    .option("startingOffsets", "earliest")
    .load()
)

parsed_df = df.selectExpr(
    "CAST(key AS STRING)", "CAST(value AS STRING)"
).select(from_json("value", schema).alias("data")).select("data.*")

# Write to parquet
write_to_parquet = (
    parsed_df.writeStream.outputMode("append")
    .format("parquet")
    .option("checkpointLocation", "checkpoint")
    .start("data/flight_events/")
)

write_to_parquet.awaitTermination()
