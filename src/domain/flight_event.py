"""
The FlightEvent module defines the schema for an individual Flight Event as a dataclass.
"""

from datetime import datetime
import logging
from src.additionals.logger import LOGGER_NAME

from .aircraft_type import AircraftType
from .geo import Point
from pydantic import BaseModel

logger = logging.getLogger(LOGGER_NAME)

class FlightEvent(BaseModel):
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
        flight_event = self.model_dump_json()
        logger.info(f"Converting Flight to Dictionary for the following flight: {self.flight_number}")
        return flight_event
