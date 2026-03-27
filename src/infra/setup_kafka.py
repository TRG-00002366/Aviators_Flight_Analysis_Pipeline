"""
Responsible for creating the `flight_events` topic in Kafka as well as handling any other configurations.
"""

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


if __name__ == "__main__":
    admin_client: KafkaAdminClient = KafkaAdminClient(bootstrap_servers="kafka:29092", client_id="topic_initialization")
    
    topic: NewTopic = NewTopic(
        name="flight_events",
        num_partitions=4,
        replication_factor=1,
        topic_configs={"retention.ms": (24*60*60*1000)}
    )

    try:
        admin_client.create_topics([topic])
        print("Topic Created???? It SHOULD be")
    except TopicAlreadyExistsError:
        print("[INFO] Topic flight_events already exists") 
