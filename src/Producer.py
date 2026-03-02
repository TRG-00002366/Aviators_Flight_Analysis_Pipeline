"""
This module defines the Producer, which will generate flight data for the application. 
It follows a multi-thread producer single-thread consumer model, which emits flight
events periodically.
"""

import threading
from datetime import datetime

THREAD_COUNT = 2

TIMESTAMP = datetime.now()

