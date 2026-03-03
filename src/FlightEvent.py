"""
The FlightEvent module defines the schema for an individual Flight Event as a dataclass.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from Point import Point

class AircraftType(Enum):
    """
    Enum for an AircraftType
    """

    B737 = "Boeing 737"
    B747 = "Boeing 747"
    B777 = "Boeing 777"
    B787 = "Boeing 787"
    A320 = "Airbus A320"
    A321 = "Airbus A321"
    A330 = "Airbus A330"
    A350 = "Airbus A350"
    A380 = "Airbus A380"
    E175 = "Embraer 175"
    E190 = "Embraer 190"
    CRJ9 = "Bombardier CRJ-900"


@dataclass
class FlightEvent:
    flight_nubmer: str  # Example: "UAL94"
    aircraft_type: AircraftType
    bearing: float
    location: Point
    elevation: float
    ground_speed: float
    timestamp: datetime
