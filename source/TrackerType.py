"""Defines TrackerType Enum object"""

from enum import Enum

class TrackerType(Enum):
    """Enumeration of the posible single object trackers"""
    KCF = 0
    MOSSE = 1
    CSRT = 2
