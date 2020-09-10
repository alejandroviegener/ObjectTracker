"""Define Multitracker as a collection of single trackers

    Typical usage:

        multi_tracker = MultiTracker()   
        
        tracker = cv.TrackerMOSSE_create()
        tracker.init(initial_frame, bbox1)
        multi_tracker.add()

        tracker = cv.TrackerMOSSE_create()
        tracker.init(initial_frame, bbox2)
        multi_tracker.add()

        for frame in frames:
            track_status_list, bbox_list = multi_tracker.update(frame)
"""

class MultiTracker:
    """Collection of single object trackers"""

    def __init__(self):
        """Initialize an empty list of trackers"""
        self.trackers = []

    def add(self, tracker):
        """Add tracker to trackers list"""
        self.trackers.append(tracker)
    
    def update(self, frame):
        """Update each of the trackers in the list
        
        Returns:
            A list containing the track status and the bbox for each tracker
        """

        # Create empty lists of track status and bounding boxes        
        track_status_list = []
        bounding_boxes = []

        # Update each tracker in the multi trackers list
        for tracker in self.trackers:
            track_status, bounding_box = tracker.update(frame)
            bounding_box = tuple([int(i) for i in bounding_box])
            track_status_list.append(track_status)
            bounding_boxes.append(bounding_box)
        
        return (track_status_list, bounding_boxes)
