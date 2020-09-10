"""Implements some utility functions
"""

import json


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
