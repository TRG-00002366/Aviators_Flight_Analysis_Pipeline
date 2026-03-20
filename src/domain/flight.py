"""
This module defines the Flight model for this DE application. It provides the "main" function
`new_random_flight` which generates flights.
"""

import math
import random
import logging
from src.additionals.logger import LOGGER_NAME
from collections.abc import Generator
from datetime import datetime, timedelta

from .geo import Point
from geodistpy import geodist, interpolate
from pydantic import BaseModel, ConfigDict

from src.utils import calculate_bearing

from .aircraft_type import AircraftType
from .flight_event import FlightEvent
from .flight_sector import FlightSector

logger = logging.getLogger(LOGGER_NAME)

class FlightCounter():
    model_config = ConfigDict(use_enum_values=True)
    airline_list = ["AS", "AA", "AC", "AM", "CO", "DL", "FX", "HA", "NW", "PO", "SW", "UA", "UPS", "VIR"]

    airline_flightNum = {
        code: 1 
        for code in airline_list
    } 

    def new_flight_number(self) -> str:
        airline: str = random.choice(self.airline_list)
        airline_num: str = f"{airline}{self.airline_flightNum[airline]}" 
        self.airline_flightNum[airline] += 1
        return airline_num
   
fc = FlightCounter() 

class Flight(BaseModel):
    """
    Dataclass representing a flight.

    Attributes:
        flight_number (str): Flight number
        origin_point (Point): Origin location.
        final_point (Point): Destination location.
        aircraft_type (AircraftType): Type of aircraft.
        flight_events (list[FlightEvent]): Events associated with the flight.
        speed_kts (float): Cruise speed in **kts** (knots).
    """
    
    origin_point: Point
    final_point: Point
    aircraft_type: AircraftType
    flight_events: Generator[FlightEvent, None, None]
    speed_kts: float
    flight_number: str


    @classmethod
    def new_random_flight(cls, initial_timestamp: datetime):
        """
        Generates and returns a new random `Flight` instance.

        Arguments:
            initial_timestamp (datetime): 
                The starting timestamp dictating when the flight first enters the airspace
            flight_number (str): 
                The string reperesentation for the flight number this flight is assigned

        Returns:
            A single `Flight` instance
        """
        boundary_choices: list[str] = random.sample(
            ["north", "south", "east", "west"], 2
        )
        entry_boundary: str = boundary_choices[0]
        exit_boundary: str = boundary_choices[1]
        
        logger.info(f"New Flight's entry and exit boundaries selected -> Entry: {entry_boundary}, Exit: {exit_boundary}")

        origin_point: Point = FlightSector.gen_random_point_boundary(entry_boundary)
        final_point: Point = FlightSector.gen_random_point_boundary(exit_boundary)
        
        logger.info(f"Origin and Final Points created -> Origin: {origin_point}, Final: {final_point}")

        aircraft_type: AircraftType = random.choice(list(AircraftType))
        speed_kts: float = random.uniform(430, 560)
        bearing: float = calculate_bearing(origin_point, final_point)

        logger.info(
            f"Created/Calculated: Aircraft Type: {aircraft_type.value}, Speed (Knots): {speed_kts}, Bearing: {bearing}"
        )

        num_points: int = math.floor(
            float(
                geodist(
                    coords1=(origin_point.latitude, origin_point.longitude),
                    coords2=(final_point.latitude, final_point.longitude),
                    metric="km",
                )
                / (speed_kts * 1.852001 * (1 / 3600))
            )
        )

        logger.info(
            f"Generating {num_points} Flight Events for Flight's Duration in Airspace"
        )
        
        points: Generator[Point, None, None] = (
            Point(longitude=long, latitude=lat)
            for (lat, long) in interpolate(
                (origin_point.latitude, origin_point.longitude),
                (final_point.latitude, final_point.longitude),
                num_points,
            )
        )
    
        logger.info(
            "Points along flight path generated"
        )
    
        elevation: int = random.randrange(30000, 40000, 1000)
        
        logger.info(
            f"Elevation choses: {elevation}"
        )
       
        flight_number = fc.new_flight_number()
        
        flight_events: Generator[FlightEvent, None, None] = (
            FlightEvent(
                flight_number=flight_number,
                aircraft_type=aircraft_type,
                bearing=bearing,
                location=point,
                elevation=elevation,
                ground_speed=speed_kts,
                timestamp=initial_timestamp + timedelta(seconds=t),
            )
            for t, point in enumerate(points)
        )
            
        logger.info(
            "Flight Events generated, proceeding to instantiate and return new Flight"
        )
        
        return cls(
            origin_point=origin_point,
            final_point=final_point,
            aircraft_type=aircraft_type,
            flight_events=flight_events,
            speed_kts=speed_kts,
            flight_number=flight_number,
        )
