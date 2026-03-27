from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct


spark = SparkSession.builder \
    .appName("spark_streaming_consumer") \
    .master("spark://spark:7077") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0"  # <- adjust Scala version if needed
    ).getOrCreate()


# Read from Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "flight_events")
    .option("startingOffsets", "earliest")
    .load()
)

# Kafka values are bytes, decode them (assuming JSON with flight_id)
from pyspark.sql.functions import from_json, approxCountDistinct
from pyspark.sql.types import StructType, StringType

schema = StructType().add("flight_number", StringType())

json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Count distinct flight_ids (active flights) continuously
active_flights = json_df.groupBy().agg(approxCountDistinct("flight_number").alias("active_flights"))

# Write live stats to console every 5 seconds
query = (
    active_flights.writeStream
    .outputMode("complete")  # needed for aggregation
    .format("console")
    .trigger(processingTime="5 seconds")
    .start()
)

query.awaitTermination()
