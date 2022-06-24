# Personal project
__author__ = "Eolus"

# Standard libraries
import datetime
import cv2
import time
from typing import Tuple
# Third party libraries
# Custom libraries


class CameraHandler:
    def __init__(self, camera_address: str, camera_name: str,
                 frames_per_minute: int, is_video_stream: bool, display_image: bool = False) -> None:
        # Camera details
        self.camera_address = camera_address
        self.camera_name = camera_name
        self.frames_per_minute = float(frames_per_minute)
        self.time_between_frames = 1 / (frames_per_minute/60)
        self.display_image = display_image
        self.is_video_stream = is_video_stream

        # Class configuration
        self.wait_key_delay = 20  # ms
        self.key_to_stop = 27  # ESC is mapped to 27
        self.retry_delay = 2  # s

        # State variables
        self.keep_running = True
        self.last_frame_time = datetime.datetime.now()

        # Queue object

    def run(self) -> None:
        while self.keep_running:
            print(f"Connecting to {self.camera_address}")
            try:
                cam_stream, rval = self.__cam_stream_init(self.camera_address,
                                                          self.camera_name,
                                                          self.display_image)

                # Loop for getting the images
                while rval and self.keep_running:
                    # Just getting pictures to avoid delay
                    if self.is_video_stream:
                        rval, f1 = cam_stream.read()
                    
                    # Checking if a wanted frame
                    frame_is_wanted = self.__is_wanted_frame()
                    if frame_is_wanted:
                        rval, f1 = cam_stream.read()
                        
                        if self.display_image:
                            cv2.imshow(self.camera_name, f1)

                            key = cv2.waitKey(self.wait_key_delay)
                            if key == self.key_to_stop:
                                self.keep_running = False
                        
                        # TODO: PLACEHOLDER FOR THE FRAME TO GET INTO THE QUEUE
                    
                    else:
                        # The frame is not wanted yet
                        time.sleep(0.02)

                print(f"Camera is not available, keep trying every {self.retry_delay}")
                time.sleep(self.retry_delay)

            except Exception as inst:
                print(f"Error while trying to connect to camera: {inst}")
                cv2.destroyWindow(self.camera_name)

        cv2.destroyWindow(self.camera_name)

    @staticmethod
    def __cam_stream_init(camera_address: str, camera_name: str, display_image: True) \
            -> Tuple[cv2.VideoCapture, bool]:
        # Initialization of the cam
        cam_stream = cv2.VideoCapture(camera_address)
        if display_image:
            cv2.namedWindow(camera_name)
        if cam_stream.isOpened():
            rval, f0 = cam_stream.read()
        else:
            rval = False

        return cam_stream, rval

    def __is_wanted_frame(self) -> bool:
        current_time = datetime.datetime.now()
        time_delta = current_time-self.last_frame_time
        if time_delta.total_seconds() >= self.time_between_frames:
            frame_is_wanted = True
            self.last_frame_time = current_time
        else:
            frame_is_wanted = False

        return frame_is_wanted

import cv2
import numpy as np
import urllib

stream=urllib.urlopen('http://96.10.1.168/mjpg/video.mjpg')
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8') # JPEG start
    b = bytes.find('\xff\xd9') # JPEG end
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2] # actual image
        bytes= bytes[b+2:] # other informations

        # decode to colored image ( another option is cv2.IMREAD_GRAYSCALE )
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow('Window name',img) # display image while receiving data
        if cv2.waitKey(1) ==27: # if user hit esc
            exit(0) # exit program