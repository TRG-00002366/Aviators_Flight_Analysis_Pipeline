import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections.abc import Generator

from .AircraftType import AircraftType
from .FlightEvent import FlightEvent
from .FlightSector import FlightSector
from geodistpy import geodist, interpolate 
from src.geo import Point
from src.utils import calculate_bearing


@dataclass
class Flight:
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
    def new_random_flight(cls, initial_timestamp: datetime, flight_number: str):
        boundary_choices: list[str] = random.sample(["north", "south", "east", "west"], 2)
        start_boundary: str = boundary_choices[0]
        end_boundary: str = boundary_choices[1]

        origin_point: Point = FlightSector.gen_random_point_boundary(start_boundary)
        final_point: Point = FlightSector.gen_random_point_boundary(end_boundary)
        
        aircraft_type: AircraftType = random.choice(list(AircraftType))
        speed_kts: float = random.uniform(430, 560)

        bearing: float = calculate_bearing(origin_point, final_point)

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

        points: Generator[Point, None, None] = (
            Point(longitude=long, latitude=lat)
            for (lat, long) in interpolate(
                (origin_point.latitude, origin_point.longitude),
                (final_point.latitude, final_point.longitude),
                num_points,
            )
        )

        elevation: int = random.randrange(30000, 40000, 1000)
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
        
        return cls(
            origin_point=origin_point,
            final_point=final_point,
            aircraft_type=aircraft_type,
            flight_events=flight_events,
            speed_kts=speed_kts,
            flight_number=flight_number,
        )
