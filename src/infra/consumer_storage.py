import json
from aiokafka import AIOKafkaConsumer
import asyncio


def create_consumer(bootstrap_servers="localhost:9092", group_id="analytics_group"):
    # Returns a Kafka Consumer
    return AIOKafkaConsumer(
        "flight_events",
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


async def main():
    # Create our consumer and subcribe to a topic
    consumer = create_consumer(group_id="storage_group")

    await consumer.start()
    try:
        with open("flight_events.json", "a") as f:
            async for msg in consumer:
                event = msg.value
                f.write(json.dumps(event) + "\n")
                print("Stored Event")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
