"""Tests the utils module"""

import pytest
import utils


@pytest.mark.parametrize("file",
                         [ ("tests/data/foo.avi"),
                           ("tests/data/empty_video_file.avi")
                         ])
def test_get_video_capture(file):
    """Test video capture method with invalid input files"""
   
   # Test with non existing file
    with pytest.raises(ValueError):
        utils.get_video_capture(file)


def test_video_capture_getters():
    """Tests all the video property getters implemented in utils"""

    frame, capture = utils.get_video_capture("tests/data/input.mkv")
    assert utils.get_video_fps(capture) == 25
    assert utils.get_video_frame_count(capture) == 250
    assert utils.get_video_frame_height(capture) == 1080
    assert utils.get_video_frame_width(capture) == 1920


def test_read_objects_to_track_file():
    """Test the reader of the objects to track file"""

    result = utils.read_objects_to_track_file("tests/data/utils_objects_to_track_test.json")
    pattern = [ 
                {"object": "player", "id": 0, "coordinates": (630, 875, 146, 212)},
                {"object": "player", "id": 1, "coordinates": (1650, 555, 152, 200)}
              ]

    for d, p in zip(result, pattern):
        assert d == p

