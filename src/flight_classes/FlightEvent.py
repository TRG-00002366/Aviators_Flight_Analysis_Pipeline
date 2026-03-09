"""
The FlightEvent module defines the schema for an individual Flight Event as a dataclass.
"""

from dataclasses import dataclass
from datetime import datetime

from .AircraftType import AircraftType
from src.geo import Point


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
    
    def to_dict(self):
        return {
           "aircraft_type": self.aircraft_type,
           "bearing": self.bearing,
           "location": {
               "latitude": self.location.latitude,
               "longitude": self.location.longitude
           },
           "elevation": self.elevation,
           "ground_speed": self.ground_speed,
           "timestamp": self.timestamp
        }
