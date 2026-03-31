"""
Responsible for pulling flight events from the flight_events topic and sending them off to Snowflake's DB.
"""
import json
from snowflake.ingest.streaming import StreamingIngestClient
from kafka import KafkaConsumer

if __name__ == "__main__":
    # ADDED: value_deserializer to automatically parse Kafka bytes into a Python dict
    kafka_consumer: KafkaConsumer = KafkaConsumer(
        'flight_events',
        bootstrap_servers="kafka:29092",
        client_id="Snowpipe_Consumer",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    with StreamingIngestClient(
        client_name="I_AM_THE_CLIENT",
        db_name="FLIGHT_EVENTS_DB",
        schema_name="BRONZE",
        pipe_name="RAW_FLIGHT_EVENTS-STREAMING",
        profile_json="profile.json"
    ) as client:
        
        with client.open_channel("A_CHANNEL")[0] as channel:
            # counter: int = 0
            for message in kafka_consumer:
                # if counter < 10:
                    # FIXED: 1. Uppercase key to match Snowflake
                    # FIXED: 2. message.value instead of message
                    # FIXED: 3. Added the required string token (message.offset)
                    channel.append_row(
                        {
                            "FLIGHT_EVENT_DATA": message.value
                        },
                        str(message.offset)
                    )
                #     counter += 1
                    # print(f"Streamed message {counter}/10")
                    # else:
                    # break