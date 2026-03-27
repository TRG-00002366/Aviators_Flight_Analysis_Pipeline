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
        bootstrap_servers='kafka:29092'
    )
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
