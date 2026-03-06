from dataclasses import dataclass


@dataclass
class FlightSector:
    north: float = 42.5
    south: float = 37.0
    east: float = -87.5
    west: float = -91.5
