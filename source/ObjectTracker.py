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

from TrackerType import TrackerType
from  MultiTracker import MultiTracker
import cv2 as cv

class ObjectTracker:
    """This class implements a video tracker for multiple objects"""

    def __init__(self, tracker_type = TrackerType.CSRT):
        self.tracker_type = tracker_type

    def track_objects(self, video_file, objects_to_track):
        """Tracks objects in a video file given the initial bounding boxes

        Args:
            video_file: video file 
            objects_info: list of dictionaries that define the objects to track. Each element of the list must have
                the following structure:
                        
                    {
                        "object": (string) description of the object to track,
                        "id": (int) id of the object to track
                        "coordinates": (tuple) coordinates of the initial bounding box (x, y, width, height)
                    }

        Returns:
            A list containing the object trackings. Each element of the list is
            a dictionary with the following structure:

                {
                    "object": (string) object description as defined in the "object_to_track" input parameter,
                    "id": (int) object id as defined in the "object_to_track" input parameter,
                    "track": list of dicts containing the info of the track result for each frame. See structure below. 
                }

                Each element of the track list has the following structure:
                   
                    {
                       "track_status": the track status, True if tracked ok, False if track lost
                       "coordinates": tuple defining the bounding box, (x, y, witdh, height)
                    } 

        Raises:
            ValueError: if video file can not be opened
            ValueError: if no frame can be read from the video
            
        """

        # Create a video capture object to read videos and verify it is open
        first_frame, video_capture = self._get_video_capture(video_file)

        # Initialize tracker with every object to track
        initial_bounding_boxes = [obj["coordinates"] for obj in objects_to_track]
        tracker = self._initialize_tracker(initial_bounding_boxes, first_frame)

        # Create object_trackings structure to be returned
        object_trackings = []
        for obj in objects_to_track:
            object_track = {"object": obj["object"], "id": obj["id"], "track": []}
            object_trackings.append(object_track)

        # Update tracking info for every frame in the video capture
        while video_capture.isOpened():

            # Read frame from video, 
            read_ok, frame = video_capture.read()
            
            # If end of video, then break
            if not read_ok:
                break

            # Track  objects in new frame and update history
            track_status_list, bounding_boxes = tracker.update(frame)
            print(track_status_list)
            for track_status, bounding_box, object_track in zip(track_status_list, bounding_boxes, object_trackings):
                track_item ={"track_status": track_status, "coordinates": bounding_box}
                object_track["track"].append(track_item)

        # Release the capture
        video_capture.release()

        # Return the object trackings
        return object_trackings

        
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
            tracker = self._create_tracker_by_type(self.tracker_type)
            tracker.init(frame, bounding_box)
            multi_tracker.add(tracker)
        
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

    @staticmethod
    def _get_video_capture(video_file):
        """Gets the video capture object and the first frame of it
        
        Args: 
            video_file: the video file
        
        Returns:
            (first_frame, video_capture)

        Raises:
            ValueError: if video file can not be opened
            ValueError: if no frame can be read from the video

        """  

        video_capture = cv.VideoCapture(video_file)
        if video_capture.isOpened() == False:
            # log message
            raise ValueError("Video file could not be opened")

        # Read first frame
        read_ok, first_frame = video_capture.read()
        if not read_ok:
            raise ValueError("Video file corrupted")

        return (first_frame, video_capture)


import utils

if __name__ == "__main__":
    """Usage example"""
    
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
