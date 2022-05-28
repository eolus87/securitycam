# Personal project
__author__ = "Eolus"

# Standard libraries
import datetime
import cv2
import time
# Third party libraries
# Custom libraries
from camera.frame import Frame


class CameraHandler:
    def __init__(self, camera_address: str, camera_name: str,
                 frames_per_minute: int, display_image: bool = False) -> None:
        # Camera details
        self.camera_address = camera_address
        self.camera_name = camera_name
        self.frames_per_minute = float(frames_per_minute)
        self.time_between_frames = 1 / (frames_per_minute/60)
        self.display_image = display_image

        # Class configuration
        self.wait_key_delay = 20  # ms
        self.key_to_stop = 27  # ESC is mapped to 27
        self.stability_sleep = 0.01  # s

        # State variables
        self.keep_running = True
        self.last_frame_time = datetime.datetime.now()

    def run(self) -> None:
        while self.keep_running:
            try:
                # Initialization of the cam
                cam_stream = cv2.VideoCapture(self.camera_address)
                if self.display_image:
                    cv2.namedWindow(self.camera_name)
                if cam_stream.isOpened():
                    rval, f0 = cam_stream.read()
                else:
                    rval = False

                # Loop for getting the images
                while rval and self.keep_running:
                    rval, f1 = cam_stream.read()
                    frame_is_wanted = self.__is_wanted_frame()

                    if self.display_image and frame_is_wanted:
                        cv2.imshow(self.camera_name, f1)

                    # TODO: PLACEHOLDER FOR THE FRAME TO GET INTO THE QUEUE

                    key = cv2.waitKey(self.wait_key_delay)
                    if key == self.key_to_stop:
                        self.keep_running = False

                    time.sleep(self.stability_sleep)

            except Exception as inst:
                print(f"Error while trying to connect to camera: {inst}")
                cv2.destroyWindow(self.camera_name)

        cv2.destroyWindow(self.camera_name)

    def __is_wanted_frame(self) -> bool:
        current_time = datetime.datetime.now()
        time_delta = current_time-self.last_frame_time
        if time_delta.total_seconds() >= self.time_between_frames:
            frame_is_wanted = True
            self.last_frame_time = current_time
        else:
            frame_is_wanted = False

        return frame_is_wanted

