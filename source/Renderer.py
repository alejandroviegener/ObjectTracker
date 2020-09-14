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
import utils
import cv2 as cv

class VideoCodec(Enum):
    """Available codecs"""
    MJPG = 'MJPG'
    DIVX = 'DIVX'
    XVID = 'XVID'

class VideoFormat(Enum):
    "Video Extentions"
    AVI = 'avi'
    MP4 = 'mp4'

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
        
        self._box_color = (0, 0, 255)
        self._box_line_width = 5
        self._text_color = (0, 0, 255)
        self._text_thickness = 2
        self._font_scale = 0.75
        self._text_font = cv.FONT_HERSHEY_SIMPLEX

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

    def render(self, video_file, object_trackings, out_path = ".", file_name = "out"):
        """Render a video file with the bounding boxes specified in object trackings
        
        Raises:
            ValueError: if video file can not be opened
            ValueError: if no frame can be read from the video
            ValueError: if video frame count not equal to object_trackings length
        """

        if not path.exists(out_path):
            raise ValueError("Output path does not exist")
        
        # Get video capture and first frame
        first_frame, video_capture = utils.get_video_capture(video_file)
        
        # Check that the object tracks are the same length of the video
        for obj in object_trackings:
            if utils.get_video_frame_count(video_capture) != len(obj["track"]):
                print(len(obj["track"]))
                print(utils.get_video_frame_count(video_capture))
                raise ValueError("Video frame count and object trackings must be equal")
        
        # Create video writer
        video_writer = cv.VideoWriter(  out_path + "/" + file_name + "." + self.video_format.value,
                                        cv.VideoWriter_fourcc(*self.video_codec.value), 
                                        utils.get_video_fps(video_capture), 
                                        (utils.get_video_frame_width(video_capture), utils.get_video_frame_height(video_capture))
                                     )
        
        # Add the object bounding boxes and text to every frame in the video
        frame_count = utils.get_video_frame_count(video_capture)
        frame_width = utils.get_video_frame_width(video_capture)
        frame_height = utils.get_video_frame_height(video_capture)
        frame = first_frame
        for i in range(frame_count):

            # Loop over tracked objects 
            for obj in object_trackings:                
                coordinates = obj["track"][i]["coordinates"]
                track_status = obj["track"][i]["track_status"]
                if track_status:

                    # Add rectangle over object
                    point1 = (coordinates[0], coordinates[1])
                    point2 = (coordinates[0] + coordinates[2], coordinates[1] + coordinates[3])
                    cv.rectangle(frame, point1, point2, self._box_color, self._box_line_width)

                    # Add text for object
                    # Text is shown UNDER the bbox unless it goes out of the video frame
                    # In that case it is shown OVER the bbox
                    text = obj["object"] + "_" + str(obj["id"])
                    x = coordinates[0]
                    y_under = coordinates[1] + coordinates[3] + 30
                    y_over = coordinates[1] - 20
                    point = (x, y_over) if y_under >= frame_height else (x, y_under)
                    cv.putText(frame, text, point, self._text_font, self._font_scale, self._text_color, self._text_thickness)
                else:
                    # Indicate a tracking error ocurred
                    point = (60, 50)
                    text = "Tracking failure: one or more objects could not be tracked"
                    cv.putText(frame, text, point, self._text_font, self._font_scale, self._text_color, self._text_thickness)

            # Write frame to output video
            video_writer.write(frame)

            # Read new frame 
            success, frame = video_capture.read()


#######################################################################
####################### Usage Example #################################
#######################################################################

from ObjectTracker import ObjectTracker
from TrackerType import TrackerType

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
