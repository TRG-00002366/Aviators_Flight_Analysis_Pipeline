"""
This module defines the Producer, which will generate flight data for the application. 
It follows an async model.
"""

import asyncio
import uuid
from datetime import datetime

from src.flight_classes import Flight

async def flight_emitter_task():
    print("Hey, I'm a task and I'm starting some work!")
    flight: Flight = Flight.new_random_flight(datetime.now(), str(uuid.uuid1(node=None, clock_seq=None)))
    for event in flight.flight_events:
        print(f"Flight: {event.flight_number}")
        await asyncio.sleep(1)

async def a_main():
    print("here")
    tasks = set()
    N = 2
    for i in range(0, N):
        task = asyncio.create_task(flight_emitter_task())
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    print("here - starting loop")
    while True:
        if len(tasks) < N:
           for i in range(0, N - len(tasks)):
               task = asyncio.create_task(flight_emitter_task())
               tasks.add(task)
               task.add_done_callback(tasks.discard)
        await asyncio.sleep(0.1)
               
asyncio.run(a_main())