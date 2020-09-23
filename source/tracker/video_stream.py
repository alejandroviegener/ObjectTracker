
import cv2 as cv
import logging
from tracker.types import VideoCodec, VideoFormat
from tracker import root_logger

# Define logger for this module
logger = logging.getLogger(root_logger.LOGGER_NAME + ".video_stream")

class FileInVideoStream:

    def __init__(self, video_file): 
        # Open capture
        try:
            self.video_capture = cv.VideoCapture(video_file)
        except:
            raise ValueError("Video file could not be opened")

    def __iter__(self):

        # Read frame
        for i in range(len(self)):
            read_ok, frame = self.video_capture.read()
            if not read_ok:
                raise StopIteration()
            
            yield (i, frame)
            i = i + 1

    def __len__(self):
        return self.get_video_frame_count()

    def get_video_fps(self):
        """Get video frame per seconds"""
        return int(self.video_capture.get(cv.CAP_PROP_FPS))

    def get_video_frame_width(self):
        """Get video frame width"""
        return int(self.video_capture.get(cv.CAP_PROP_FRAME_WIDTH))

    def get_video_frame_height(self):
        """Get video frame height"""
        return int(self.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT))

    def get_video_frame_count(self):
        """Get video frame count"""
        return int(self.video_capture.get(cv.CAP_PROP_FRAME_COUNT))


class FileOutVideoStream():

    def __init__(self, file_name, width = 600, height = 600, fps = 25, out_path = "."):
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

        # Create video writer
        self.video_writer = cv.VideoWriter(  out_path + "/" + file_name + "." + self.video_format.value,
                                             cv.VideoWriter_fourcc(*self.video_codec.value), 
                                             fps, 
                                             (width, height)
                                          )

        # Log data
        logger.info(f"File out video stream initialized")
    
    def save(self, frame):
        # Write frame to output video
        self.video_writer.write(frame)


import time
if __name__ == "__main__":
        
    # Create input stream 
    video_file = "../../data/input.mkv"
    stream = FileInVideoStream(video_file)

    
    for (i, frame) in stream:
        # Display result
        cv.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv.waitKey(1) & 0xff
        if k == 27 : break
