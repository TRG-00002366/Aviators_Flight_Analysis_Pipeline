"""
This module defines the Producer, which will generate flight data for the application. 
It follows an async model.
"""

import asyncio
import uuid
import logging
from datetime import datetime

from aiokafka import AIOKafkaProducer

from src.domain.flight import Flight
from src.additionals.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

async def flight_task(producer: AIOKafkaProducer) -> None:
    flight: Flight = Flight.new_random_flight(datetime.now())
    logger.info(f"Emitting flight {flight.flight_number} ")
    
    for event in flight.flight_events:
        logger.debug(f"Flight {event.flight_number} -> lat={event.location.latitude}, lon={event.location.longitude}")
        await producer.send("flight_events", event.model_dump_json().encode("utf-8"))
        await asyncio.sleep(1)

    logger.debug(f"Flight {flight.flight_number} fully emitted")

def create_task(producer: AIOKafkaProducer, tasks: set) -> None:
    task = asyncio.create_task(flight_task(producer))
    tasks.add(task)
    task.add_done_callback(tasks.discard)
    logger.debug(f"Task {task.get_name()} started")

async def main():
    logger.info("Producer connecting...")
    producer: AIOKafkaProducer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    logger.info("Producer connected")

    tasks = set()
    N = 4

    for i in range(0, N):
        create_task(producer, tasks)
    logger.info(f"Started {N} workers")

    try:
        while True:
            while len(tasks) < N:
                create_task(producer, tasks) 
            await asyncio.sleep(0.1)
    finally:
        logger.info("Shutting down producer...")
        await producer.stop()
        logger.info("Producer stopped")

asyncio.run(main())