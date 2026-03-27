from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType

def run_flight_count_job():
    # Initialize Spark INSIDE the function
    spark = SparkSession.builder.appName("simple analysis").master("local[*]").getOrCreate()

    schema = StructType([
        StructField("flight_number", StringType()),
        StructField("aircraft_type", StringType()),
        StructField("bearing", FloatType()),
        StructField("location", StructType([
            StructField("longitude", FloatType()),
            StructField("latitude", FloatType()),
        ])),
        StructField("elevation", FloatType()),
        StructField("ground_speed", FloatType()),
        StructField("timestamp", TimestampType()),
    ])

    # Ensure this path matches your Ubuntu/Docker volume mapping
    df = spark.read.schema(schema).parquet("/opt/airflow/data/flight_events/")

    flight_count = df.count()
    count_df = spark.createDataFrame([(flight_count,)], ["total_count"])
    count_df.write.mode("overwrite").parquet("/opt/airflow/data/number_of_flights")