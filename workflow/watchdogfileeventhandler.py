# Personal Project
__author__ = "Eolus"

# Standard libraries
import os
import re
import queue
from watchdog.events import FileSystemEventHandler
# Third party libraries
# Custom libraries
from data_classes.cameraconfchange import CameraConfChange
from data_classes.cameraconfchangeenum import CameraConfChangeEnum


class WatchdogFileEventHandler(FileSystemEventHandler):
    def __init__(self, events_queue: queue.Queue, file_pattern: str) -> None:
        self.__events_queue = events_queue
        self.__file_pattern = file_pattern

    def on_moved(self, event):
        print(f"\nMoved file detected! {event.src_path}")
        self.__check_and_add_to_queue(event, CameraConfChangeEnum.NEW)

    def on_created(self, event):
        print(f"\nCreated file detected! {event.src_path}")
        self.__check_and_add_to_queue(event, CameraConfChangeEnum.NEW)

    def on_deleted(self, event):
        print(f"\nDeleted file! {event.src_path}")
        self.__check_and_add_to_queue(event, CameraConfChangeEnum.DELETED)

    def on_modified(self, event):
        print(f"\nFile modified! {event.src_path}")
        self.__check_and_add_to_queue(event, CameraConfChangeEnum.DELETED)
        self.__check_and_add_to_queue(event, CameraConfChangeEnum.NEW)

    def on_closed(self, event):
        pass

    def __check_and_add_to_queue(self, event,
                                 type_of_change: CameraConfChangeEnum) -> None:
        file_changed = os.path.basename(event.src_path)
        pattern_found = re.search(self.__file_pattern, file_changed)
        try:
            if pattern_found is not None:
                conf_change = CameraConfChange(event.src_path,
                                               type_of_change)
                self.__events_queue.put(conf_change)
        except Exception as inst:
            print(f"\nError while processing {event}: {inst}")
