# Add imports for all necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import array_max, array_min, avg, cast, col, count, substr, when, desc



spark = SparkSession.builder().appName("smth").getOrCreate()

df = spark.read.parquet("data/flight_events/")
rdd = df.rdd


# Average time in airspace(per aircraft type?)
# Take first and last timestamp for each flight and calculate duration
# May break with array_max/min
flight_time = df.withColumn(
    "total_flight_time",
    array_max("timestamps").cast("long") - array_min("timestamps").cast("long"),
)
avg_duration = flight_time.groupBy("total_flight_time").agg(avg("total_flight_time"))

avg_duration.write.mode("overwirte").parquet("data/avg_duration")

# Busiest time of day
# TWEAK: USE FIRST TIMESTAMP HOUR
# calculate avg flights per hour then find the hour with the highest average
df = df.withColumn("hour", df["timestamp"].cast("timestamp").substr(12, 2).cast("int"))
avg_flights_per_hour = df.groupBy("hour").count()
busiest_hour = avg_flights_per_hour.orderBy("count", ascending=False).first()
busiest_hour.write.mode("overwrite").parquet("data/buisiest_hour")

# most common aircraft type
most_common_aircraft = (
    df.groupBy("aircraft_type").count().orderBy("count", ascending=False).first()
)
most_common_aircraft.write.mode("overwrite").parquet("data/most_common_aircraft")


# most common direction in and out
# use bearing to determine direction convert to N/S/E/W
# calculate most common direction
direction = df.withColumn(
    "direction",
    when((col("bearing") >= 315) | (col("bearing") < 45), "N")
    .when((col("bearing") >= 45) & (col("bearing") < 135), "E")
    .when((col("bearing") >= 135) & (col("bearing") < 225), "S")
    .otherwise("W")
)

direction_counts = direction.groupby("direction").count()
most_common_direction = direction_counts.orderby(desc("count")).first()
most_common_direction.write.mode("overwrite").parqet("data/most_common_direction")

# Possibly add graphs for visualization


#crash detection flights within 5 miles horizontal and 1000ft vert



#distance traveld over time


#Density per square mile


#Average cruise speed per aircraft
avg_speed = df.groupby("aircraft_type").agg(avg("speed"))
avg_speed.write.mode("overwrite").parquet("data/avg_speed")
