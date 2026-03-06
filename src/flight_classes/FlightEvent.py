"""
The FlightEvent module defines the schema for an individual Flight Event as a dataclass.
"""

from dataclasses import dataclass
from datetime import datetime

from .AircraftType import AircraftType
from .Point import Point


@dataclass
class FlightEvent:
    """
    Dataclass for a Flight Event

    Attributes:
        flight_number: `str`
        aircraft_type: `AircraftType`
        bearing: `float`
        location: `Point`
        elevation: `float`
        ground_speed: `float`
        timestamp: `datetime`

    """

    flight_number: str  # Example: "UAL94"
    aircraft_type: AircraftType
    bearing: float
    location: Point
    elevation: float
    ground_speed: float
    timestamp: datetime
