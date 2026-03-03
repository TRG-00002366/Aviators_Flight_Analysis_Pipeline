"""
This module defines the Producer, which will generate flight data for the application. 
It follows a multi-thread producer single-thread consumer model, which emits flight
events periodically.
"""

import threading
import queue
from datetime import datetime

PARTIES = 2

TIMESTAMP = datetime.now()

EMIT_BARRIER = threading.Barrier(parties=PARTIES)

QUEUE = queue.Queue()

def task():
    while True:
        print("hello")
        EMIT_BARRIER.wait()

threads = [threading.Thread(target=task) for i in range(0,2)]

