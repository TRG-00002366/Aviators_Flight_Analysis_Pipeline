from geodistpy import interpolate, geodist
import math
from datetime import datetime, timedelta
import random
from dataclasses import dataclass

flight_num_tracker = 1
aircraft_types = [
    "Boeing 737",
    "Boeing 747",
    "Boeing 777",
    "Boeing 787",
    "Airbus A320",
    "Airbus A330",
    "Airbus A350",
    "Airbus A380"
]

top_left = (89.0, 42.0)
top_right = (87.0, 42.0)
bottom_left = (89.0, 40.0)
bottom_right = (87.0, 40.0)

initial_timestamp = datetime.now()

@dataclass
class Flight:
    flight_num: int
    aircraft_type: str
    bearing: str
    location: tuple[float, float]
    altitude: float
    speed: float

def gen_initial_location():
    return random.choice(
        [
            (random.choice([87.0, 89.0]), random.uniform(40.0, 42.0)),
            (random.uniform(87.0, 89.0), random.choice([40.0, 42.0]))
        ]
    )
    
def gen_final_location(initial_location):
    if initial_location[0] in {87.0, 89.0}:
        return random.choice(
            [
                
            ]
        )
def gen_new_flight_lifetime():
    flight_num = flight_num_tracker 
    flight_num += 1
    aircraft_type = random.choice(aircraft_types)
    initial_location = gen_initial_location()
    final_location = 
    altitude = random.randrange(10000, 40000, 1000)
    speed = random.randrange(200, 800, 10)
    
    
    
def generate_flight_events():
    """    
    To generate flight events, we need to calculate a flight path. Dependant on the flight path, we need to
    figure out how many events we have to generate. We'll be generating per second. To 
    calculate this, we need:
        - Longitude (Initial)
        - Latitude (Initial)
        - Heading (Initial)
        - Speed
        
    Give the intial longitude, latitiude, and heading, we can define the flight path as starting from one
    boundary to another. Then, given the speed, we can compute how many events ought to be generated and 
    compute the flight events. 
    """
    
    # First, we need to find the flight path. Ergo, we need to compute the start and the end. To compute
    # this, we need a beginning and an ending - boundary to boundary. How do we do this? We first ought to define
    # a boundary. Let's do a rectangle : (89 W, 42 N), (89 W, 40 N), (87 W, 40 N), (87 W, 42 N)
    # Now that we have a rectangle, we need a way to compute possible starting points along the boundary lines.
    # We'll do random and only do to maybe 1 decimal spot. 
    # We'll then use the Haversine formula to get the distance. We get the speed and divide d/s to get how many
    # seconds it takes for the plane to travel. Assign the quotient to n and interpolate n points. 
    top_right = (89.0, 42.0)
    bottom_left = (87.0, 40.0)
    start_time = datetime.now()
    next_time = start_time + timedelta(seconds=1)
    distance = geodist(top_right, bottom_left, metric="km")
    n = math.floor(distance / 100)
    points = interpolate(top_right, bottom_left, n)
    
    return f"Distance: {distance}\nPoints: {points}\nTimestamps = {start_time},{next_time}"
    
print(generate_flight_events())
