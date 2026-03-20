from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule # Added this
from datetime import datetime, timedelta
# Import the specific function
from src.analytics.batch_rdd_etl import run_flight_count_job 
from src.analytics.batch_df_etl import avg_flight, busiest_tod, most_common_aircraft, most_common_direction, avg_cruise_speed

with DAG(
    "simple_summary",
    schedule=timedelta(minutes=5),
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    start = EmptyOperator(task_id="start")
    
    flight_count = PythonOperator(
        task_id="run_flight_count",
        python_callable=run_flight_count_job # Point to the function, not the module
    )

    avg_flight_time = PythonOperator(
        task_id="avg_flight",
        python_callable=avg_flight # Point to the function, not the module
    )


    end = EmptyOperator(
        task_id="end",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    start >> [flight_count, avg_flight_time] >> end
