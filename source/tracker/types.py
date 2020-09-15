"""Defines TrackerType Enum object"""

from enum import Enum

class VideoCodec(Enum):
    """Available codecs"""
    MJPG = 'MJPG'
    DIVX = 'DIVX'
    XVID = 'XVID'

class VideoFormat(Enum):
    "Video Extentions"
    AVI = 'avi'
    MP4 = 'mp4'

class TrackerType(Enum):
    """Enumeration of the posible single object trackers"""
    KCF = 0
    MOSSE = 1
    CSRT = 2
