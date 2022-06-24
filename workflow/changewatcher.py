# Personal Project
__author__ = "Eolus"

# Standard libraries
import queue
import re
import os
from watchdog.observers import Observer
# Third party libraries
# Custom libraries
from data_classes.cameraconfchange import CameraConfChange
from data_classes.cameraconfchangeenum import CameraConfChangeEnum
from workflow.watchdogfileeventhandler import WatchdogFileEventHandler


class ChangeWatcher:
    def __init__(self, camera_confs_path: str, camera_confs_pattern: str,
                 changes_queue: queue.Queue, watchdog_instance: WatchdogFileEventHandler) -> None:
        self.camera_confs_path = camera_confs_path
        self.camera_confs_pattern = camera_confs_pattern

        self.__init_first_time(changes_queue)

        self.watchdog_instance = watchdog_instance
        self.observer = Observer()
        self.observer.schedule(self.watchdog_instance, camera_confs_path, recursive=False)
        self.observer.start()

    def __init_first_time(self, changes_queue: queue.Queue) -> None:
        initial_configuration_files = [f for f in os.listdir(self.camera_confs_path)
                                       if re.search(self.camera_confs_pattern, f)]
        initial_configuration_files = [os.path.join(self.camera_confs_path, x) for x in initial_configuration_files]
        for i in range(len(initial_configuration_files)):
            try:
                changes_queue.put(CameraConfChange(initial_configuration_files[i],
                                                   CameraConfChangeEnum.NEW))
            except Exception as inst:
                print(f"Error while loading camera conf located in: "
                      f"{initial_configuration_files[i]}, {inst}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
