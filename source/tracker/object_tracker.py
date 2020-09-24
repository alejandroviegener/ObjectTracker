"""This class implements a video tracker for multiple objects

    Given a video file and initial bounding boxes, the class generates for every frame and every initial boundig box,
    the corresponding tracking bounding box. 

    Example usage:

        video_file = "../data/input.mkv"
        objects_to_track_file = "../data/initial_conditions.json"
        tracker_type = TrackerType.MOSSE

        # Read file with objects to track 
        objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)
        print("Objects to track: ", objects_to_track)

        # Create tracker and track the objects
        tracker = ObjectTracker(tracker_type)
        object_trackings = tracker.track_objects(video_file, objects_to_track)

"""

from tracker.types import TrackerType
from  tracker.multi_tracker import MultiTracker
import cv2 as cv
from tracker import utils
import logging
from tracker import root_logger

# Define logger for this module
logger = logging.getLogger(root_logger.LOGGER_NAME + ".object_tracker")


class ObjectTracker:
    """This class implements a video tracker for multiple objects"""

    def __init__(self, tracker_type = TrackerType.CSRT):
        self.tracker_type = tracker_type
        self.bounding_boxes = None
        self.frame_index = 0
        self.tracker = None
        logger.info(f"Object tracker {tracker_type.name} initialized")

    def set_objects_to_track(self, bounding_boxes):
        self.bounding_boxes = bounding_boxes

    def reset(self):
        self.frame_index = 0

    def update(self, frame):
        if self.frame_index == 0:
            self.tracker = self._initialize_tracker(self.bounding_boxes, frame)
            self.frame_index += 1
            return ( [True] * len(self.bounding_boxes), self.bounding_boxes)
        else:
            self.frame_index += 1
            return self.tracker.update(frame)

    def _initialize_tracker(self, initial_bounding_boxes, frame):
        """Returns a multitracker object
        
        Args:
            initial_bounding_boxes: initial box for each object
            frame: initial frame where the objecs are located

        Returns:
            A multitracker object
        """
        
        multi_tracker = MultiTracker()
        for bounding_box in initial_bounding_boxes:
            multi_tracker.add(self.tracker_type, frame, bounding_box)
        
        logger.info(f"Multi tracker initialized for {len(initial_bounding_boxes)} objects")
        return multi_tracker


    @staticmethod
    def _create_tracker_by_type(tracker_type):
        """Returns a single tracker object according to the type parameter"""
        
        tracker = None
        if tracker_type == TrackerType.KCF:
            tracker = cv.TrackerKCF_create()
        elif tracker_type == TrackerType.MOSSE:
            tracker = cv.TrackerMOSSE_create()
        elif tracker_type == TrackerType.CSRT:
            tracker = cv.TrackerCSRT_create()
        else:
            tracker = cv.TrackerCSRT_create()

        return tracker


#######################################################################
####################### Usage Example #################################
#######################################################################
if __name__ == "__main_______":
    
    video_file = "../data/input.mkv"
    objects_to_track_file = "../data/initial_conditions.json"
    tracker_type = TrackerType.MOSSE

    objects_to_track = utils.read_objects_to_track_file(objects_to_track_file)
    print("Objects to track: ", objects_to_track)

    tracker = ObjectTracker(tracker_type)
    object_trackings = tracker.track_objects(video_file, objects_to_track)

    for tracking in object_trackings:
        print(tracking)
        print("\r\n\r\n")
