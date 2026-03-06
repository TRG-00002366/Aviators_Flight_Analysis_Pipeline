# Add imports for all necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, substr, cast, array_max, array_min

# Decide what analysis to perform
# pull data from csv/json
df = spark.read.json("Json name")


# Average time in airspace(per aircraft type?)
# Take first and last timestamp for each flight and calculate duration
# May break with array_max/min
flight_time = df.withColumn(
    "total_flight_time",
    array_max("timestamps").cast("long") - array_min("timestamps").cast("long")
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
