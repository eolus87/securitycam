__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import datetime
import cv2
# Third party libraries
# Custom libraries
from data_classes.cameraconf import CameraConf
from data_classes.frame import Frame


class FileInterface:
    def __init__(self, camera_conf: CameraConf) -> None:
        self.camera_name = camera_conf.name
        self.storing_path = os.path.normpath(camera_conf.store_path)
        self.file_extension = ".png"

    def store(self, frame: Frame, extra_details: str = "") -> None:
        # Naming
        datetime_now = datetime.datetime.now().strftime("%y%m%d_%H%M%S-%f")
        date_now = datetime_now.split("_")[0]
        time_now = datetime_now.split("_")[1]

        # Folder and naming
        folder_path = os.path.join(self.storing_path, self.camera_name, date_now)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(
            folder_path,
            time_now + extra_details + self.file_extension
        )

        # Storing
        cv2.imwrite(file_path, frame.values)
