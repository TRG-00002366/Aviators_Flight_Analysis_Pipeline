import time
from datetime import datetime
from .Flight import Flight
start = time.time()
f = Flight.new_random_flight(datetime.now(), "UAL1")
print(f"Generated {len(f.flight_events)} events in {time.time() - start:.4f}s")