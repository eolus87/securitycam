__author__ = "Eolus"

# Standard libraries
import time
# Third party libraries
import numpy as np
# Custom libraries
from camera.filevideostream import FileVideoStream
from data_classes.cameraconf import CameraConf
from processing.motiondetector import MotionDetector
from interfaces.fileinterface import FileInterface
from utilities.init_logger import init_logger
from processing.peopledetector import PeopleDetector


class Orchestrator:
    """This class is used to orchestrate the different services."""
    def __init__(self):
        """Initializes the class. It is done just for sanity with the variables that will
        be populated later in the initialization method
        """
        self.__logger = None
        self.__file_video_stream = None
        self.__motion_detector = None
        self.__people_detector = None
        self.__file_interface = None
        self.__keep_running = True
        self.__camera_name = ""

    def initialization(self, camera_conf: CameraConf, shared_dict: dict) -> None:
        """Initializes the class. It starts the different services.
        This method is not intended to be called directly. It is called by the start method.
        It should have been an __init__ method, but it is not possible due to a limitation
        with the multiprocessing library.

        :param camera_conf: CameraConf object with the camera configuration.
        :param shared_dict: Dictionary to share the frames between processes.
        """
        # Initialization of logger
        self.__logger = init_logger(camera_conf.generic_conf.name)

        # Initialization of services
        self.__file_video_stream = FileVideoStream(camera_conf)
        frame_object = self.__file_video_stream.read()
        shared_dict[frame_object.cam_name] = np.copy(frame_object.values)

        self.__motion_detector = MotionDetector(camera_conf)
        self.__people_detector = PeopleDetector(camera_conf)

        self.__file_interface = FileInterface(camera_conf)

        # Other variables
        self.__camera_name = camera_conf.generic_conf.name

    def start(self, camera_conf: CameraConf, shared_dict: dict) -> None:
        """Starts the flow of the camera.
        This method starts the video stream and the different services.
        """
        self.initialization(camera_conf, shared_dict)

        self.__file_video_stream.start()

        while self.__keep_running:
            if self.__file_video_stream.more():
                # tic = time.time()
                frame_object = self.__file_video_stream.read()
                shared_dict[frame_object.cam_name] = np.copy(frame_object.values)

                motion_detected, frame_with_detection = \
                    self.__motion_detector.detect_motion(frame_object)
                people_detected, frame_with_people_detection = \
                    self.__people_detector.detect_people(frame_object)
                if motion_detected:
                    self.__file_interface.store(frame_with_detection, "motion")
                if people_detected:
                    self.__file_interface.store(frame_with_people_detection, "people")

                # toc = time.time() - tic
                # print(f"{self.__camera_name}: Frame time {toc:.2f} s")
            else:
                time.sleep(0.02)

    def stop(self, time_out: int = 0) -> None:
        """Stops the flow of the camera.
        This method stops the video stream and the different services.

        :param time_out: Time to wait before exiting the flow.
        """
        if self.__file_video_stream is not None:
            self.__file_video_stream.stop()
        self.__keep_running = False
        time.sleep(time_out)
        self.__logger.info(f"Exiting the flow of camera: {self.__camera_name}.")
