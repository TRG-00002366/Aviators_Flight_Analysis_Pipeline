import random
import logging
from typing import ClassVar

from src.additionals.logger import LOGGER_NAME

from .geo import Point
from pydantic import BaseModel

logger = logging.getLogger(LOGGER_NAME)

class FlightSector(BaseModel):
    # north: float = 42.5
    # south: float = 37.0
    # east: float = -87.5
    # west: float = -91.5
    north: ClassVar[float] = 41.880
    south: ClassVar[float] = 41.870
    east: ClassVar[float] = -87.620
    west: ClassVar[float] = -87.630
    
    @classmethod
    def gen_random_point_boundary(cls, boundary_choice: str):
        long: float
        lat: float
        match boundary_choice:
            case "north":
                long = random.uniform(cls.west, cls.east)
                lat = cls.north
            case "south":
                long = random.uniform(cls.west, cls.east)
                lat = cls.south
            case "east":
                long = cls.east
                lat = random.uniform(cls.south, cls.north)
            case _:
                long = cls.west
                lat = random.uniform(cls.south, cls.north)
        
        p: Point = Point(latitude=lat, longitude=long)
        logger.info(f"Created random boundary point on {boundary_choice}: {p}")
        return p
        