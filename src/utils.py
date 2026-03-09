"""
A suite of helper functions used across the codebase.
"""

import math

from src.domain.geo import Point

def calculate_bearing(origin_point: Point, final_point: Point) -> float:
    """
    Calcuates the straight-line bearing between two geo-graphical points:
        
    Arguments:
        origin_point (Point): The origin `Point`
        final_point (Point): The destination `Point`
        
    Returns:
        bearing (float): In Degrees
    """
    lat1: float = math.radians(origin_point.latitude)
    long1: float = math.radians(origin_point.longitude)
    lat2: float = math.radians(final_point.latitude)
    long2: float = math.radians(final_point.longitude)

    bearing_rad: float = math.atan2(
        math.sin(long2 - long1) * math.cos(lat2),
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1),
    )

    return round((math.degrees(bearing_rad) + 360) % 360, 2)