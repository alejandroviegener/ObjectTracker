import numpy as np
import cv2 as cv


video_file = "data/input.mkv"
video_capture = cv.VideoCapture(video_file)

ret, frame = video_capture.read()

cv.imshow("VideoFrame", frame)
cv.waitKey(0)
video_capture.release()
cv.destroyAllWindows()