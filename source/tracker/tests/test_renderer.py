"""Tests the renderer module"""

import pytest
from tracker.renderer import BoundingBoxRenderer
import json
import numpy as np
from tracker.types import TrackerType
from tracker import utils
import cv2 as cv

@pytest.fixture(scope="module")
def renderer():
    """Creates a BoundingBoxRenderer"""
    renderer = BoundingBoxRenderer()
    return renderer


@pytest.mark.parametrize("color, line_width",
                         [ ((255, 255, 255), 0),
                           ((255, 255, 255), -1), 
                           ((255, 255, -1), 2),
                           ((255, 255, 256), 2)
                         ])
def test_set_box_format(renderer, color, line_width):
    """Test box format setter with invalid colors and line widths"""

    # Line width must be possitive
    with pytest.raises(ValueError):
        renderer.set_box_format(color, line_width)


@pytest.mark.parametrize("color, line_width, scale",
                    [ ((255, 255, 255), 0, 1),
                    ((255, 255, 255), -1, 1), 
                    ((255, 255, -1), 2, 1),
                    ((255, 255, 256), 2, 1),
                    ((255, 255, 255), 2, 0),
                    ((255, 255, 255), 2, -1)
                    ])
def test_set_text_format(renderer, color, line_width, scale):
    """Test text format setter with invalid colors and line widths"""

    # Line width must be possitive
    with pytest.raises(ValueError):
        renderer.set_text_format(color, line_width, scale)


def test_renderer(renderer):
    """Test bounding box render"""    
    
    # Read unrendered video and render 
    video_file = "tests/data/input.mkv"
    tracker_type = TrackerType.KCF

    # Read trackings for each object
    with open("tests/data/input_trackings.json") as f:
        object_trackings = json.load(f)
    
    # Render video
    renderer = BoundingBoxRenderer()
    renderer.set_box_format((0, 255, 0), 2)
    renderer.set_text_format((255, 255, 255), 2, 0.8)
    renderer.render(video_file, object_trackings, out_path="tests/data", file_name="render_test_output")

    # Read rendered video and reference
    render = cv.VideoCapture("tests/data/render_test_output.avi")
    render_pattern = cv.VideoCapture("tests/data/render_test_pattern_dock.avi")

    # Compare each frame of the rendered video with the render reference pattern
    is_ok_1, frame_1 = render.read()
    is_ok_2, frame_2 = render_pattern.read()
    while is_ok_1 and is_ok_2:

        difference = cv.subtract(frame_1, frame_2)
        b, g, r = cv.split(difference)
        assert np.count_nonzero(b) == 0 and np.count_nonzero(g) == 0 and np.count_nonzero(r) == 0

        is_ok_1, frame_1 = render.read()
        is_ok_2, frame_2 = render_pattern.read()
