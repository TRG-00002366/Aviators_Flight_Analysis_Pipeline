from dataclasses import dataclass
from turtle import st

from numba.core.typing.builtins import StaticGetItemClass
from FlightEvent import FlightEvent
from Point import Point
from FlightSector import FlightSector
from datetime import datetime
import geodistpy
import random

flight_sector = FlightSector()
choices = {
    "north": flight_sector.north,
    "south": flight_sector.south,
    "east": flight_sector.east,
    "west": flight_sector.west
}

@dataclass
class Flight:
    origin_point: Point
    final_point: Point
    aircraft_type: str
    flight_events: list[FlightEvent]
    speed: float
   
    @classmethod
    def new_random_flight(cls, initial_timestamp: datetime):
        # 1. Find a random origin and destination
        start_boundary, end_boundary = random.sample(list(choices.items()), 2)
       
        # start maps to origin, end maps to final
        boundary_to_point = {
            start_boundary: Point(0.0, 0.0),
            end_boundary: Point(0.0, 0.)
        }
        
        for boundary in boundary_to_point.keys():
            if boundary[0] in ["north", "south"]:
               boundary_to_point[boundary] = Point(
                   random.uniform(choices["east"], choices["west"]),
                   choices[boundary[0]]
               ) 
            else:
                boundary_to_point[boundary] = Point(
                    choices[boundary[0]],
                    random.uniform(choices["south"], choices["north"])
                )
       
        origin_point: Point = boundary_to_point[start_boundary]
        final_point: Point = boundary_to_point[end_boundary]