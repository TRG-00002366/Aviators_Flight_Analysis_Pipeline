import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from .AircraftType import AircraftType
from .FlightEvent import FlightEvent
from .FlightSector import FlightSector
from geodistpy import geodist, interpolate
from .Point import Point


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
        speed (float): Cruise speed in **kts** (knots).
    """

    origin_point: Point
    final_point: Point
    aircraft_type: AircraftType
    flight_events: list[FlightEvent]
    speed: float
    flight_number: str

    @classmethod
    def new_random_flight(cls, initial_timestamp: datetime, flight_number: str):
        choices: list[str] = ["north", "south", "east", "west"]
        start_and_end: list[str] = random.sample(choices, 2)
        start_boundary: str = start_and_end[0]
        end_boundary: str = start_and_end[1]

        flight_sector: FlightSector = FlightSector()
        origin_point: Point = Point.gen_random_point_boundary(
            start_boundary, flight_sector
        )
        final_point: Point = Point.gen_random_point_boundary(
            end_boundary, flight_sector
        )
        aircraft_type: AircraftType = random.choice(list(AircraftType))
        speed: float = random.uniform(430, 560)

        # Watch this buckaroo, we bout to calculate bearing
        lat1: float = math.radians(origin_point.latitude)
        long1: float = math.radians(origin_point.longitude)
        lat2: float = math.radians(final_point.latitude)
        long2: float = math.radians(final_point.longitude)

        bearing_rad: float = math.atan2(
            math.sin(long2 - long1) * math.cos(lat2),
            math.cos(lat1) * math.sin(lat2)
            - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1),
        )

        bearing: float = round((math.degrees(bearing_rad) + 360) % 360, 2)

        num_points: int = math.floor(
            float(
                geodist(
                    coords1=(origin_point.latitude, origin_point.longitude),
                    coords2=(final_point.latitude, final_point.longitude),
                    metric="km",
                )
                / (speed * 1.852001 * (1 / 3600))
            )
        )

        points: list[Point] = [
            Point(longitude=long, latitude=lat)
            for (lat, long) in interpolate(
                (origin_point.latitude, origin_point.longitude),
                (final_point.latitude, final_point.longitude),
                num_points,
            )
        ]

        elevation: int = random.randrange(30000, 40000, 1000)
        flight_events = [
            FlightEvent(
                flight_number=flight_number,
                aircraft_type=aircraft_type,
                bearing=bearing,
                location=point,
                elevation=elevation,
                ground_speed=speed,
                timestamp=initial_timestamp + timedelta(seconds=t),
            )
            for t, point in enumerate(points)
        ]

        return Flight(
            origin_point=origin_point,
            final_point=final_point,
            aircraft_type=aircraft_type,
            flight_events=flight_events,
            speed=speed,
            flight_number=flight_number,
        )
