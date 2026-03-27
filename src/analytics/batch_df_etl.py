# Add imports for all necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import array_max, array_min, avg, cast, col, count, substr
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType


spark = SparkSession.builder.appName("smth").getOrCreate()



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

df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

# Average time in airspace(per aircraft type?)
# Take first and last timestamp for each flight and calculate duration
# May break with array_max/min
def avg_flight():
    spark = SparkSession.builder.appName("smth").getOrCreate()

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

    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

    flight_times = df.groupBy("flight_number").agg(
        min("timestamp").alias("entry_time"),
        max("timestamp").alias("exit_time")
    )

    flight_times = flight_times.withColumn(
        "duration_seconds",
        col("exit_time").cast("long") - col("entry_time").cast("long")
    )

    avg_time = flight_times.agg(
        avg("duration_seconds").alias("avg_duration_seconds")
    )

    avg_time.write.mode("overwrite").parquet("data/avg_duration")

# Busiest time of day
# TWEAK: USE FIRST TIMESTAMP HOUR
# calculate avg flights per hour then find the hour with the highest average
def busiest_tod():
    spark = SparkSession.builder.appName("smth").getOrCreate()

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

    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

    df = df.withColumn("hour", df["timestamp"].cast("timestamp").substr(12, 2).cast("int"))
    avg_flights_per_hour = df.groupBy("hour").count()
    busiest_hour = avg_flights_per_hour.orderBy("count", ascending=False).first()
    busiest_hour.write.mode("overwrite").parquet("data/buisiest_hour")

# most common aircraft type
def most_common_aircraft():
    spark = SparkSession.builder.appName("smth").getOrCreate()

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

    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

    most_common_aircraft = (
        df.groupBy("aircraft_type").count().orderBy("count", ascending=False).first()
    )
    most_common_aircraft.write.mode("overwrite").parquet("data/most_common_aircraft")


# most common direction in and out
# use bearing to determine direction convert to N/S/E/W
# calculate most common direction
def most_common_direction():
    spark = SparkSession.builder.appName("smth").getOrCreate()

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

    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

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
def avg_cruise_speed():
    spark = SparkSession.builder.appName("smth").getOrCreate()

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

    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

    avg_speed = df.groupby("aircraft_type").agg(avg("speed_kts"))
    avg_speed.write.mode("overwrite").parquet("data/avg_speed")
