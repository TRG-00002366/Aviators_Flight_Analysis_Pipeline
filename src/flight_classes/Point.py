import random
from dataclasses import dataclass

from .FlightSector import FlightSector


@dataclass
class Point:
    longitude: float
    latitude: float

    # This returns a type Point, but I wish I knew how to annotate it
    @classmethod
    def gen_random_point_boundary(cls, boundary_choice: str, fs: FlightSector):
        match boundary_choice:
            case "north":
                return Point(
                    longitude=random.uniform(fs.west, fs.east), latitude=fs.north
                )
            case "south":
                return Point(
                    longitude=random.uniform(fs.west, fs.east), latitude=fs.south
                )
            case "east":
                return Point(
                    longitude=fs.east, latitude=random.uniform(fs.south, fs.north)
                )
            case _:
                return Point(
                    longitude=fs.west, latitude=random.uniform(fs.south, fs.north)
                )
