"""
This module defines the enum type for an Aircraft - the aircraft type, that is.
"""

from enum import Enum


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
