"""Implements a Bounding Box Renderer that adds a bounding box on each frame of a video
given the object tracking history

Typical usage:

    renderer = BoundingBoxRenderer()
    renderer.set_box_format((0, 255, 0), 2)
    renderer.set_text_format((255, 255, 255), 2, 0.8)
    renderer.render(video_file, object_trackings, out_path=".", file_name="out")    

    The object_trackings history can be obtained with the ObjectTracker class.

"""


import platform
from enum import Enum
from os import path
from tracker import utils
import cv2 as cv
import logging
from tracker import root_logger
from tracker.types import VideoCodec, VideoFormat

# Define logger for this module
logger = logging.getLogger(root_logger.LOGGER_NAME + ".bounding_box_render")

class BoundingBoxRenderer:

    def __init__(self):
        """Inititialize codec and format according to the system running"""
        
        system = platform.system()
        if system == "Darwin":
            self.video_codec = VideoCodec.MJPG
            self.video_format = VideoFormat.AVI
        elif system == "Linux":
            self.video_codec = VideoCodec.XVID
            self.video_format = VideoFormat.AVI
        elif system == "Windows":
            self.video_codec = VideoCodec.DIVX
            self.video_format = VideoFormat.AVI
        else:
            self.video_codec = VideoCodec.DIVX
            self.video_format = VideoFormat.AVI
        
        self._box_color = (0, 255, 255)
        self._box_line_width = 5
        self._text_color = (255, 255, 255)
        self._text_thickness = 2
        self._font_scale = 0.75
        self._text_font = cv.FONT_HERSHEY_SIMPLEX

        # Log data
        logger.info(f"Renderer initialized")

    def set_box_format(self, color, line_width):
        """Set bounding box color and line width
        
        Raise:
            ValueError if line width less than 1
            ValueError if color no valid
        """
        
        # Preconditions
        if line_width < 1:
            raise ValueError("Invalid line width") 
        for c in color:
            if c < 0 or c > 255:
                raise ValueError("Invalid color value")

        self._box_color = color
        self._box_line_width = line_width
        logger.debug(f"Set box format, color: {color}, line width: {line_width}")

    def set_text_format(self, color, thickness, scale, font=cv.FONT_HERSHEY_SIMPLEX):
        """Set bounding box color and line width
         Raise:
            ValueError if line width less than 0
            ValueError if color no valid
            ValueError if scale is not positive
        """
        
        # Preconditions
        if thickness <= 0:
            raise ValueError("Invalid thickeness") 
        if scale <= 0:
            raise ValueError("Scale must be a positive value")
        for c in color:
            if c < 0 or c > 255:
                raise ValueError("Invalid color value")

        self._text_color = color
        self._text_thickness = thickness
        self._font_scale = scale
        logger.debug(f"Set text format, color: {color}, thikness: {thickness}, scale: {scale}")


    def frame_update(self, frame, boxes, track_status, object_ids = None):
        
        # Create object ids if not defined
        if object_ids is None:
            object_ids = range(len(boxes))
       
        # Loop over boxes and statuses 
        for status, coordinates, obj_id in zip(track_status, boxes, object_ids):                
            if status:

                # Add rectangle over object
                point1 = (coordinates[0], coordinates[1])
                point2 = (coordinates[0] + coordinates[2], coordinates[1] + coordinates[3])
                cv.rectangle(frame, point1, point2, self._box_color, self._box_line_width)

                # Add text for object
                # Text is shown UNDER the bbox unless it goes out of the video frame
                # In that case it is shown OVER the bbox
                text = "object" + "_" + str(obj_id)
                x = coordinates[0]
                y_under = coordinates[1] + coordinates[3] + 30
                y_over = coordinates[1] - 20
                point = (x, y_over) if y_under >= frame.shape[0] else (x, y_under)
                cv.putText(frame, text, point, self._text_font, self._font_scale, self._text_color, self._text_thickness)
            else:
                # Indicate a tracking error ocurred
                point = (60, 50)
                text = "Tracking failure: one or more objects could not be tracked"
                cv.putText(frame, text, point, self._text_font, self._font_scale, self._text_color, self._text_thickness)


#######################################################################
####################### Usage Example #################################
#######################################################################

from tracker.object_tracker import ObjectTracker
from tracker.types import TrackerType
import json

if __name__ == "__main__":

    video_file = "../data/input.mkv"
    objects_to_track_file = "../data/initial_conditions.json"
    tracker_type = TrackerType.KCF

    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)
    print("Objects to track: ", objects_to_track)

    # Create trackings for each object
    tracker = ObjectTracker(tracker_type)
    object_trackings = tracker.track_objects(video_file, objects_to_track)
    
    # Render video
    renderer = BoundingBoxRenderer()
    renderer.set_box_format((0, 255, 0), 2)
    renderer.set_text_format((255, 255, 255), 2, 0.8)
    renderer.render(video_file, object_trackings, out_path=".", file_name="out")

    #with open("trackings.json", "w") as f:
    #    json.dump(object_trackings, f)
