"""
Responsible for pulling flight events from the flight_events topic and sending them off to Snowflake's DB.
"""
import time

from snowflake.ingest.streaming import StreamingIngestClient
from kafka import KafkaConsumer

if __name__ == "__main__":
    kafka_consumer: KafkaConsumer = KafkaConsumer(
        'flight_events',
        bootstrap_servers="kafka:29092",
        client_id="Snowpipe_Consumer"
    )
    
    with StreamingIngestClient(
        client_name="I_AM_THE_CLIENT",
        db_name="FLIGHT_EVENTS_DB",
        schema_name="BRONZE",
        pipe_name="FLIGHT_EVENTS_PIPE",
        profile_json="profile.json"
    ) as client:
        
        with client.open_channel("A_CHANNEL")[0] as channel:
            counter: int = 0
            for message in kafka_consumer:
                if counter < 10:
                    channel.append_row(
                        {
                            "flight_event_data": message
                        }
                    )
                else:
                    break