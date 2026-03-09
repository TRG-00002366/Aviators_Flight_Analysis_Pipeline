from dataclasses import dataclass
import random

from src.geo import Point

@dataclass
class FlightSector:
    # north: float = 42.5
    # south: float = 37.0
    # east: float = -87.5
    # west: float = -91.5
    north: float = 41.880
    south: float = 41.870
    east: float = -87.620
    west: float = -87.630
    
    @classmethod
    def gen_random_point_boundary(cls, boundary_choice: str):
        match boundary_choice:
            case "north":
                return Point(
                    longitude=random.uniform(cls.west, cls.east), latitude=cls.north
                )
            case "south":
                return Point(
                    longitude=random.uniform(cls.west, cls.east), latitude=cls.south
                )
            case "east":
                return Point(
                    longitude=cls.east, latitude=random.uniform(cls.south, cls.north)
                )
            case _:
                return Point(
                    longitude=cls.west, latitude=random.uniform(cls.south, cls.north)
                )