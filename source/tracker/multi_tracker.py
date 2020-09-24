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


import multiprocessing as mp
import time
import cv2 as cv

class MultiTracker:
    """Collection of single object trackers"""

    processes = []
    input_queues = []
    output_queues = []
    processes_started = False

    def __init__(self):
        pass

    @staticmethod
    def add(tracker_type, frame, bounding_box):
        """Add tracker to trackers list"""

        # Create queues and process
        input_queue = mp.Queue()
        output_queue = mp.Queue()
        process = mp.Process(target=MultiTracker._track, args=(tracker_type, frame, bounding_box, input_queue, output_queue))
        
        # Store queus and processes instances
        MultiTracker.input_queues.append(input_queue)
        MultiTracker.output_queues.append(output_queue)
        MultiTracker.processes.append(process)

    @staticmethod
    def start():
        """Start all tracker processes"""
        if MultiTracker.processes_started:
            return

        for process in MultiTracker.processes :
            process.start()                  
        MultiTracker.processes_started = True

    @staticmethod
    def stop():
        if not MultiTracker.processes_started:
            return 

        for process in MultiTracker.processes:
            process.join()
        MultiTracker.processes_started = False

    @staticmethod
    def _track(tracker_type, frame, bounding_box, input_queue, output_queue):
        """Used to multiprocess"""
    
        tracker = cv.TrackerCSRT_create()
        tracker.init(frame, bounding_box)
        while True:
            new_frame = input_queue.get(True)
            track_status, bounding_box = tracker.update(new_frame)
            
            bounding_box = tuple([int(i) for i in bounding_box])
            result = (track_status,bounding_box)
            
            output_queue.put(result, True)
        
        #track_status, bounding_box = tracker.update(frame)
        #bounding_box = tuple([int(i) for i in bounding_box])
        #return (track_status, bounding_box)

    @staticmethod
    def update(frame, optimize = True):
        """Update multitracker
        
        Args:
            optimize: True to run in multiple processes, False otherwhise
        """

        if optimize:
            return MultiTracker.update_optimized(frame)
        else:
            return MultiTracker.update_not_optimized(frame)


    @staticmethod
    def update_optimized(frame):
        """Update each of the trackers in the list (multi process optimized)
        
        Returns:
            A list containing the track status and the bbox for each tracker
        """

        MultiTracker.start()

        # Create empty lists of track status and bounding boxes        
        track_status_list = []
        bounding_boxes = []

        for queue in MultiTracker.input_queues:
            queue.put(frame)

        for queue in MultiTracker.output_queues:
            status, bbox = queue.get(True)
            track_status_list.append(status)
            bounding_boxes.append(bbox)

        return (track_status_list, bounding_boxes)


    def update_not_optimized(frame):
        """Update each of the trackers in the list (not optimized)
        
        Returns:
            A list containing the track status and the bbox for each tracker
        """

        # Create empty lists of track status and bounding boxes        
        track_status_list = []
        bounding_boxes = []

        # Update each tracker in the multi trackers list
        for tracker in MultiTracker.trackers:
            track_status, bounding_box = tracker.update(frame)
            bounding_box = tuple([int(i) for i in bounding_box])
            track_status_list.append(track_status)
            bounding_boxes.append(bounding_box)
        
        return (track_status_list, bounding_boxes)
