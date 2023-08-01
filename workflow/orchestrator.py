# Personal project
__author__ = "Eolus"

# Standard libraries
import os
import queue
import time
import yaml
import threading
# Third party libraries
# Custom libraries
from workflow.changewatcher import ChangeWatcher
from data_classes.cameraconfchangeenum import CameraConfChangeEnum
from data_classes.cameraconfchange import CameraConfChange
from camera.camerahandlervideo import CameraHandlerVideo
from interfaces.fileinterface import FileInterface


class Orchestrator:
    """
    The orchestrator objective is controlling the workflow of the
    code.
    """

    def __init__(self, change_watcher: ChangeWatcher, changes_queue: queue.Queue) -> None:
        # Folder and file type to monitor
        self.change_watcher = change_watcher
        self.changes_queue = changes_queue

        self.camera_handlers = []

    def check_queue(self) -> None:
        camera_change = self.changes_queue.get()
        if camera_change is not None:
            if camera_change.action == CameraConfChangeEnum.NEW:
                print("Starting a new camera")
                camera_change = self.launch_camera(camera_change)
                self.camera_handlers.append(camera_change)
            elif camera_change.action == CameraConfChangeEnum.DELETED:
                print("Removing a camera")
                camera_handlers_confs = [x.conf_path for x in self.camera_handlers]
                index_to_remove = camera_handlers_confs.index(camera_change.conf_path)
                self.camera_handlers[index_to_remove].camera_handler.keep_running = False
                time.sleep(2)
                del self.camera_handlers[index_to_remove]
            else:
                print("Undefined action")

    def close_and_clean(self) -> None:
        # Stop the filewatcher
        self.change_watcher.stop()

        # Stop the cameras
        for camera in self.camera_handlers:
            camera.camera_handler.keep_running = False

        # Leave time to the threads to stop
        time.sleep(1)

    @staticmethod
    def launch_camera(camera_change: CameraConfChange) -> CameraConfChange:
        # %% Initialization and configuration
        pictures_queue = queue.Queue()

        with open(os.path.join(camera_change.conf_path)) as f:
            camera_details_1 = yaml.load(f, Loader=yaml.FullLoader)

        # %% Initialization of classes

        camera_handler_1 = CameraHandlerVideo(camera_details_1['address'],
                                              camera_details_1['name'],
                                              camera_details_1['frames_per_minute'],
                                              True, pictures_queue)
        picture_file_interface_1 = FileInterface(camera_details_1['name'],
                                                 camera_details_1['store_path'])
        camera_handler_1.add_customer(picture_file_interface_1)
        # %% Thread creation and While Loop
        camera_change.camera_handler = camera_handler_1
        threading.Thread(target=camera_handler_1.run, daemon=True).start()

        return camera_change
