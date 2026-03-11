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

async def flight_emitter_task():
    logger.info("Beginning flight creation")
    flight: Flight = Flight.new_random_flight(datetime.now(), str(uuid.uuid1(node=None, clock_seq=None)))
    logger.info("New random flight created")
    
    logger.info("Starting AIOKakfaProducer...")
    producer: AIOKafkaProducer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092'
    )
    await producer.start()
    logger.info("AIOKafkaProducer starting")
    
    try: 
        for event in flight.flight_events:
            # For now, we'll just log as a sign we've emitted
            logger.info(f"Sending flight event {event.flight_number} to Kafka Topic {"flight_topic"}")
            await producer.send("flight_events", event.model_dump_json().encode("utf-8"))
            await asyncio.sleep(1)
    finally:
        await producer.stop()
        
async def a_main():
    logger.info("Starting data generation...")
    tasks = set()
    N = 4
    for i in range(0, N):
        logger.debug("Creating and adding async tasks to tasks")
        task = asyncio.create_task(flight_emitter_task())
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    logger.info("Tasks added")
    while True:
        if len(tasks) < N:
           logger.info("A task has finished, adding new task for flight generation and emission")
           for i in range(N - len(tasks)):
               task = asyncio.create_task(flight_emitter_task())
               tasks.add(task)
               task.add_done_callback(tasks.discard)
               logger.info("Task added and started")
        await asyncio.sleep(0.1)
               
asyncio.run(a_main())