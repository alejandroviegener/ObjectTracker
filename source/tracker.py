
"""Application that receives a video file and initial bounging objects on the first frame
of the image and generates a video output with the object trackings

usage: tracker.py [-h] [-a {KCF,MOSSE,CSRT}] [-t n n n] [-b n n n] [-o OUT_FILE_NAME] [-v {0,1,2}] video initial_conditions

positional arguments:
  video                 Input video file
  initial_conditions    Initial conditions (json) file

optional arguments:
  -h, --help            show this help message and exit
  -a {KCF,MOSSE,CSRT}, --algorithm {KCF,MOSSE,CSRT} Tracking algorithm
  -t n n n, --text_color Text color, BGR separated by space
  -b n n n, --box_color Box color, BGR separated by space
  -o OUT_FILE_NAME, --out_file_name OUT_FILE_NAME
  -v {0,1,2}, --verbosity {0,1,2} Set output verbosity

Example: 
    python tracker.py ../data/input.mkv ../data/initial_conditions.json -a KCF -b 0 255 0 -t 255 255 255 -o output -v 1 

"""

from ObjectTracker import ObjectTracker
from TrackerType import TrackerType
from Renderer import  BoundingBoxRenderer 
import utils
import argparse
import sys

def get_tracker_type(name):
    """Return tracker type object by name"""
    if name == "KCF":
        return TrackerType.KCF
    elif name == "CSRT":
        return TrackerType.CSRT
    else:
        return TrackerType.MOSSE

def log(text, verbose_level, terminator="\n"):
    """Print if verbose is not zero"""
    if verbose_level > 0:
        print(text, end=terminator)
        sys.stdout.flush()

# Main application 
if __name__ == "__main__":
    
    # Argument parser configuration
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=str, help="Input video file")
    parser.add_argument("initial_conditions", type=str, help="Initial conditions (json) file")
    parser.add_argument("-a", "--algorithm", type=str, choices=["KCF", "MOSSE", "CSRT"], help="Tracking algorithm", default="KCF")
    parser.add_argument("-t", "--text_color", type=int, nargs=3, help="Text color, BGR separated by space", default=[255, 255, 255])
    parser.add_argument("-b", "--box_color", type=int, nargs=3, help="Box color, BGR separated by space", default=[0, 255, 0])
    parser.add_argument("-o", "--out_file_name", type=str, default="out")
    parser.add_argument("-p", "--out_path", type=str, default=".")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="Set output verbosity", default=0)
    args = parser.parse_args()

    # Read arguments
    video_file = args.video
    objects_to_track_file = args.initial_conditions
    tracker_type = get_tracker_type(args.algorithm)
    text_color = tuple(args.text_color)
    box_color = tuple(args.box_color)
    out_file_name = args.out_file_name
    out_path = args.out_path
    verbosity = args.verbosity

    log("Reading initial conditions file...", verbosity)
    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)
    log("done", verbosity)

    # Create trackings for each object
    log("Tracking objects in video...", verbosity)
    tracker = ObjectTracker(tracker_type)
    object_trackings = tracker.track_objects(video_file, objects_to_track)
    log("done", verbosity)
    
    # Render video
    log("Rendering output video...", verbosity)
    renderer = BoundingBoxRenderer()
    renderer.set_box_format(box_color, 2)
    renderer.set_text_format(text_color, 2, 0.8)
    renderer.render(video_file, object_trackings, out_path=out_path, file_name=out_file_name)
    log("done", verbosity)
