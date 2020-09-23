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

from concurrent.futures import ThreadPoolExecutor as PoolEcecutor

class MultiTracker:
    """Collection of single object trackers"""

    def __init__(self):
        """Initialize an empty list of trackers"""
        self.trackers = []

    def add(self, tracker):
        """Add tracker to trackers list"""
        self.trackers.append(tracker)
    
    @staticmethod
    def _track(parameters):
        """Used to multiprocess"""
        self = parameters[0]
        i = parameters[1]
        tracker = self.trackers[i]
        frame = parameters[2]
        track_status, bounding_box = tracker.update(frame)
        bounding_box = tuple([int(i) for i in bounding_box])
        return (track_status, bounding_box)

    def update(self, frame, optimize = False):
        """Update multitracker
        
        Args:
            optimize: True to run in multiple processes, False otherwhise
        """

        if optimize:
            return self.update_optimized(frame)
        else:
            return self.update_not_optimized(frame)

    def update_optimized(self, frame):
        """Update each of the trackers in the list (multi process optimized)
        
        Returns:
            A list containing the track status and the bbox for each tracker
        """

        # Create empty lists of track status and bounding boxes        
        track_status_list = []
        bounding_boxes = []

        # Launch each tracker in a separate process
        with PoolEcecutor(max_workers=len(self.trackers)) as executor:    
            parameters = [(self, i, frame) for i in range(len(self.trackers))]
            result = executor.map(self._track, parameters)
            
            for status, bbox in result:
                track_status_list.append(status)
                bounding_boxes.append(bbox)

        return (track_status_list, bounding_boxes)

    def update_not_optimized(self, frame):
        """Update each of the trackers in the list (not optimized)
        
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
