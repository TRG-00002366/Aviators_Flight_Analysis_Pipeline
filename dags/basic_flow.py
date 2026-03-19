from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

def run_spark_count():
    # We use the full path to uv if it's not in the Docker PATH
    from pyspark.sql import SparkSession

    spark: SparkSession = (
        SparkSession.builder.appName("simple analysis").master("local[*]").getOrCreate()
    )

    df = spark.read.parquet("data/flight_events/")
    rdd = df.rdd

    print(rdd.count())

with DAG(
    "simple_summary",
    schedule=timedelta(minutes=5), # Runs every 5 mins
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    analyze_flights = PythonOperator(
        task_id='run_batch_analysis', # Required
        python_callable=run_spark_count,
    )