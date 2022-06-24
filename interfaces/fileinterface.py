# Personal project
__author__ = "Eolus"

# Standard libraries
import os
import datetime
import cv2
# Third party libraries
# Custom libraries
from data_classes.frame import Frame


class FileInterface:
    def __init__(self, camera_name: str, storing_path: str) -> None:
        self.camera_name = camera_name
        self.storing_path = os.path.normpath(storing_path)

    def store(self, frame: Frame) -> None:
        if frame.cam_name == self.camera_name:
            # Naming
            datetime_now = datetime.datetime.now().strftime("%y%m%d_%H%M%S-%f")
            date_now = datetime_now.split("_")[0]
            time_now = datetime_now.split("_")[1]

            # Creation of the folder
            folder_path = os.path.join(self.storing_path, self.camera_name, date_now)
            os.makedirs(folder_path, exist_ok=True)

            # Storing the file
            file_path = os.path.join(folder_path, time_now)
            cv2.imwrite(file_path + ".png", frame.values)
            # TODO: Change the timestamp for the one in the dataclass
        else:
            # Nothing to do if it is not the camera name in the init
            pass

    def notify(self, frame: Frame) -> None:
        self.store(frame)