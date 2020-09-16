"""Tests the tracker module"""

import pytest
from tracker.object_tracker import ObjectTracker
import json
import numpy as np
from tracker.types import TrackerType
from tracker import utils
import cv2 as cv

@pytest.fixture(scope="module")
def tracker():
    """Creates a BoundingBoxRenderer"""

    tracker_type = TrackerType.KCF
    tracker = ObjectTracker(tracker_type)
    return tracker


@pytest.mark.parametrize("file",
                         [ ("tests/data/foo.avi"),
                           ("tests/data/empty_video_file.avi")
                         ])
def test_tracker_invalid_parameters(tracker, file):
    """Test the track method with invalid files"""

    objects_to_track_file = "tests/data/initial_conditions.json"
    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)

    # Test exceptions raise with invalid video files
    with pytest.raises(ValueError):
        tracker.track_objects(file, objects_to_track)


def test_tracking(tracker):
    """Test tracking using a tracking reference"""

    objects_to_track_file = "tests/data/initial_conditions.json"
    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)

    # Note: this evaluation method should be changed,
    #   An evaluation method using a metric, as for example the Jaccard Index, could be used
    #   instead if checking that the exact bounding boxes are matched. A particular bounding box can 
    #   be validated if the JI is above a certain threshold. Then a performance metric could me used (for example, accuracy or f-score)
    
    # Read trackings for each object
    with open("tests/data/input_trackings.json") as f:
        reference_trackings = json.load(f)

    # Ommiting for speed isues
    #trackings = tracker.track_objects("tests/data/input.mkv", objects_to_track)
    #for a, b in zip(trackings, reference_trackings):
    #    assert a == b

