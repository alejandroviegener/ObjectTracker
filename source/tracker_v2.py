
"""Application that receives a video file and initial bounding boxes on the first frame
of the image and generates a video output with the object trackings

usage: tracker [-h] [-a {KCF,MOSSE,CSRT}] [-t TEXT_COLOR TEXT_COLOR TEXT_COLOR] [-b BOX_COLOR BOX_COLOR BOX_COLOR] [-o OUT_FILE_NAME] [-v {0,1,2,3}] [-l, --log] video initial_conditions

positional arguments:
  video                 Input video file
  initial_conditions    Initial conditions (json) file

optional arguments:
  -h, --help            show this help message and exit
  -a {KCF,MOSSE,CSRT}, --algorithm {KCF,MOSSE,CSRT}
                        Tracking algorithm (default: KCF)
  -t TEXT_COLOR TEXT_COLOR TEXT_COLOR, --text_color TEXT_COLOR TEXT_COLOR TEXT_COLOR
                        Text color, BGR separated by space (default: [255, 255, 255])
  -b BOX_COLOR BOX_COLOR BOX_COLOR, --box_color BOX_COLOR BOX_COLOR BOX_COLOR
                        Box color, BGR separated by space (default: [0, 255, 0])
  -o OUT_FILE_NAME, --out_file_name OUT_FILE_NAME
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Set output verbosity (0- Error, 1 - Warning, 2 - Info, 3 - Debug) (default: 2)
  -l, --log             Log to file (default: False)

Example: 
    python tracker.py input.mkv initial_conditions.json -a MOSSE -b 0 255 0 -t 255 255 255 -o output -v 2 --log 

"""

from tracker.video_stream import FileInVideoStream
from tracker.object_tracker import ObjectTracker
from tracker.types import TrackerType
from tracker.renderer import  BoundingBoxRenderer 
from tracker import root_logger
from tracker import utils
import argparse
import sys
import logging
import cv2 as cv

# Utils functions
def get_tracker_type(name):
    """Return tracker type object by name"""
    if name == "KCF":
        return TrackerType.KCF
    elif name == "CSRT":
        return TrackerType.CSRT
    else:
        return TrackerType.MOSSE

# Create application logger
logger = logging.getLogger(root_logger.LOGGER_NAME + ".main_app")

# Some globals
in_out_path = "./in_out"
log_file = in_out_path + "/out.log"

# Main application 
if __name__ == "__main__":
    
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog="tracker", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", type=str, help="Input video file")
    parser.add_argument("initial_conditions", type=str, help="Initial conditions (json) file")
    parser.add_argument("-a", "--algorithm", type=str, choices=["KCF", "MOSSE", "CSRT"], help="Tracking algorithm", default="CSRT")
    parser.add_argument("-t", "--text_color", type=int, nargs=3, help="Text color, BGR separated by space", default=[255, 255, 255])
    parser.add_argument("-b", "--box_color", type=int, nargs=3, help="Box color, BGR separated by space", default=[0, 255, 0])
    parser.add_argument("-o", "--out_file_name", type=str, default="out")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3], help="Set output verbosity (0- Error, 1 - Warning, 2 - Info, 3 - Debug)", default=2)
    parser.add_argument("-l", "--log", default=False, action="store_true" , help="Log to file")

    args = parser.parse_args()

    # Read arguments
    video_file = in_out_path + "/" + args.video
    objects_to_track_file = in_out_path + "/" + args.initial_conditions
    tracker_type = get_tracker_type(args.algorithm)
    text_color = tuple(args.text_color)
    box_color = tuple(args.box_color)
    out_file_name = args.out_file_name
    log_to_file = args.log
    verbosity = args.verbosity

    # Configure logging verbosity
    if verbosity == 0:
        root_logger.logger.setLevel(logging.ERROR)
    elif verbosity == 1:
        root_logger.logger.setLevel(logging.WARNING)
    elif verbosity == 2:
        root_logger.logger.setLevel(logging.INFO)
    else:
        root_logger.logger.setLevel(logging.DEBUG)

    # Log to file
    if log_to_file:
        root_logger.add_file_handler(log_file)

    # Create input stream video
    in_stream = FileInVideoStream(video_file)

    # Log
    logger.info("1/3 Reading initial conditions file and configuring tracker")

    # Read initial conditions file
    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)

    # Create tracker from initial conditions
    tracker = ObjectTracker(tracker_type)
    
    # Set initial bounding boxes in tracker
    initial_bounding_boxes = [obj["coordinates"] for obj in objects_to_track]
    tracker.set_objects_to_track(initial_bounding_boxes)

    # Create bbox renderer
    renderer = BoundingBoxRenderer()

    # Log
    logger.info("2/3 Iterate over frames")

    # Iterate over input video stream and render video
    for i, frame in in_stream:
        
        # Track opjects
        status_list, bboxes = tracker.update(frame)
        
        # Add bboxes to frame 
        renderer.render_frame(frame, bboxes, status_list)

        # Show image, exit if ESC pressed
        cv.imshow("Tracking", frame)
        k = cv.waitKey(1) & 0xff
        if k == 27 : break


    # Render video
    #logger.info("3/3 Rendering output video")
    #renderer = BoundingBoxRenderer()
    #renderer.set_box_format(box_color, 2)
    #renderer.set_text_format(text_color, 2, 0.8)
    #renderer.render(video_file, object_trackings, out_path=in_out_path, file_name=out_file_name)
