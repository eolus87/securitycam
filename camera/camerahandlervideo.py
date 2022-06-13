# Personal project
__author__ = "Eolus"

# Standard libraries
import datetime
import cv2
import time
import queue
from typing import Tuple
# Third party libraries
# Custom libraries
from camera.frame import Frame


class CameraHandlerVideo:
    def __init__(self, camera_address: str, camera_name: str,
                 frames_per_minute: int, display_image: bool = False, 
                 queue_object: queue.Queue = None) -> None:
        # Camera details
        self.camera_address = camera_address
        self.camera_name = camera_name
        self.frames_per_minute = float(frames_per_minute)
        self.time_between_frames = 1 / (frames_per_minute/60)
        self.display_image = display_image

        # Class configuration
        self.wait_key_delay = 20  # ms
        self.key_to_stop = 27  # ESC is mapped to 27
        self.retry_delay = 2  # s

        # State variables
        self.keep_running = True
        self.last_frame_time = datetime.datetime.now()
        self.queue_object = queue_object

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
                        
                        if self.queue_object is not None:
                            new_frame = Frame(f1, self.camera_name)
                            self.queue_object.put(new_frame)
                    
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

