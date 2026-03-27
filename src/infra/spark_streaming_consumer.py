from pyspark.sql import SparkSession
from pyspark.sql.types import (FloatType, StringType, StructField, StructType,
                               TimestampType)
from pyspark.sql.functions import from_json

spark = (
    SparkSession.builder.appName("spark_streaming_consumer") # pyright: ignore[reportAttributeAccessIssue]
    .master("spark://spark:7077")
    #.config("--packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0")
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
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "flight_events")
    .option("startingOffsets", "earliest")
    .load()
)

parsed_df = df.selectExpr(
    "CAST(key AS STRING)", "CAST(value AS STRING)"
).select(from_json("value", schema).alias("data")).select("data.*")

"""
parsed_df.writeStream.outputMode("append")
.trigger(processingTime="5 seconds")
.format("parquet")
.option("checkpointLocation", "/mounted-data/data/checkpoint")
.start("/mounted-data/data/flight_events/")
"""
# Write to parquet
write_to_parquet = (
    parsed_df.writeStream.outputMode("append")
    .trigger(processingTime="5 seconds")
    .format("parquet")
    .option("checkpointLocation", "/mounted-data/data/checkpoint")
    .start("/mounted-data/data/flight_events/")
)

write_to_parquet.awaitTermination()