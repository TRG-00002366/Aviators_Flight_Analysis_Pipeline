# Add imports for all necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import array_max, array_min, avg, cast, col, count, substr


# Decide what analysis to perform
# pull data from csv/json
def create_consumer(bootstrap_servers="localhost:9092", group_id="analytics_group"):
    # Returns a Kafka Consumer
    return KafkaConsumer(
        # Bootstraps servers for my kafka brokers
        bootstrap_servers=bootstrap_servers,
        # Controls the consumer group. As a reminder, memebers of the same consumer group can be assigned to different
        # partitions to achieve parallelism
        group_id=group_id,
        # Additional details (Review on your own)
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
    )


# Average time in airspace(per aircraft type?)
# Take first and last timestamp for each flight and calculate duration
# May break with array_max/min
flight_time = df.withColumn(
    "total_flight_time",
    array_max("timestamps").cast("long") - array_min("timestamps").cast("long"),
)
avg_duration = flight_time.groupBy("total_flight_time").agg(avg("total_flight_time"))

# Number of flights
num_flights = df.count()

# Busiest time of day
# TWEAK: USE FIRST TIMESTAMP HOUR
# calculate avg flights per hour then find the hour with the highest average
df = df.withColumn("hour", df["timestamp"].cast("timestamp").substr(12, 2).cast("int"))
avg_flights_per_hour = df.groupBy("hour").count()
busiest_hour = avg_flights_per_hour.orderBy("count", ascending=False).first()

# most common aircraft type
most_common_aircraft = (
    df.groupBy("aircraft_type").count().orderBy("count", ascending=False).first()
)

# most common direction in and out
# use bearing to determine direction convert to N/S/E/W
# calculate most common direction

# Possibly add graphs for visualization
