"""Test script for multitracking

This script is not inteded to be rigorous in software good practices
The script is used to learn about the OpenCV lib and in particular about the its Tracker API

Source:  https://www.learnopencv.com/multitracker-multiple-object-tracking-using-opencv-c-python/

Usage:

    Open a terminal go to the source file dir and type:
        python 02_opencv-multi-tracker-test.py

    Select a Tracker from the list  
    The video is displayed while the objects are tracked. The rendered video is generated in the same folder (out.mkv)
"""

import sys
import cv2
from random import randint
import json

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:    
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]: 
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)
    
    return tracker


# Select tracker
print("Tracker list:")
for i, tracker in enumerate(trackerTypes):
    print( "  " + str(i) + " - " + tracker)
user_input = input("Select tracker:")

# Specify the tracker type
trackerType = trackerTypes[int(user_input)] 

# Set video to load
videoPath = "videos/run.mp4"

# Create a video capture object to read videos
cap = cv2.VideoCapture("../../data/input.mkv")

# Define the codec and create VideoWriter object
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(w)
print(h)
print(fps)
out = cv2.VideoWriter(  'out.mp4',
                        cv2.VideoWriter_fourcc(*'DIVX'),  #cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 
                        int(fps), 
                        (int(w),  int(h))
                   )

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
    print('Failed to read video')
    sys.exit()

# Read file that contains the bounding boxes to track
json_file = "../../data/initial_conditions.json"
with open(json_file) as f:
    initial_conditions = json.load(f)

## Select boxes
bboxes = []
colors = [] 

for obj in initial_conditions:
    coordinates = tuple(obj["coordinates"])
    bboxes.append(coordinates)
    
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    colors.append(color)

print('Selected bounding boxes {}'.format(bboxes)) 

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker 
for bbox in bboxes:
    tracker = createTrackerByName(trackerType)
    multiTracker.add(tracker, frame, bbox)

# Process video and track objects
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
  
    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)

    # draw tracked objects
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

    # show frame
    cv2.imshow('MultiTracker', frame)
  
    # Save video
    out.write(frame)

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break



    
# Release the capture
cap.release()
out.release()
