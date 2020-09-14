"""Implements some utility functions
"""

import json
import cv2 as cv

def read_objects_to_track_file(json_file):
    """Reads a json file and returns a list of dictionaries containing the objects to track info
    
    The file is expected to be in the following format:
        [
            {
                "object": "player",
                "id": 0,
                "coordinates": [
                    630,
                    875,
                    146,
                    212
                ]
            },
            
             ...
        ]

        coordinates are in the format (x, y, width, heigth)

    The returned list elements have the following format:

        {
            "object": (string) description of the object to track,
            "id": (int) id of the object to track
            "coordinates": (tuple) coordinates of the initial bounding box (x, y, width, height)
        }
    """

    objects_to_track = None
    with open(json_file) as f:
        objects_to_track = json.load(f)

    for obj in objects_to_track:
        obj["coordinates"] = tuple(obj["coordinates"])
        obj["id"] = int(obj["id"])
        obj["object"] = str(obj["object"])
    
    return objects_to_track


def get_video_capture(video_file):
    """Gets the video capture object and the first frame of it
    
    Args: 
        video_file: the video file
    
    Returns:
        (first_frame, video_capture)

    Raises:
        ValueError: if video file can not be opened
        ValueError: if video file has no frame
    """  
    
    # Open capture
    try:
        video_capture = cv.VideoCapture(video_file)
    except:
        raise ValueError("Video file could not be opened")

    # Read first frame
    read_ok, first_frame = video_capture.read()
    if not read_ok:
        raise ValueError("Empty video file")

    return (first_frame, video_capture)


def get_video_fps(video_capture):
    """Get video frame per seconds"""
    return int(video_capture.get(cv.CAP_PROP_FPS))

def get_video_frame_width(video_capture):
    """Get video frame width"""
    return int(video_capture.get(cv.CAP_PROP_FRAME_WIDTH))

def get_video_frame_height(video_capture):
    """Get video frame height"""
    return int(video_capture.get(cv.CAP_PROP_FRAME_HEIGHT))

def get_video_frame_count(video_capture):
    """Get video frame count"""
    return int(video_capture.get(cv.CAP_PROP_FRAME_COUNT))
    