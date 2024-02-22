__author__ = "Eolus"

# Standard libraries
from threading import Thread
from queue import Queue
import logging
import time
import re
# Third party libraries
import cv2
import numpy as np
# Custom libraries
from data_classes.frame import Frame
from data_classes.cameraconf import CameraConf

RECONNECTION_RETRY_DELAY = 60  # s
SLEEP_TIME_BETWEEN_FRAMES = 0.02  # s 30 fps = 0.0333, but time.sleep is not precise
FRAME_QUEUE_SIZE = 128
DUMMY_FRAME_WIDTH = 960
DUMMY_FRAME_HEIGHT = 540


class FileVideoStream:
    """This class has been very influenced by pyimagesearch blog!
    It is a class that allows to read a video file in a different thread. """
    def __init__(self, camera_conf: CameraConf, queue_size: int = FRAME_QUEUE_SIZE) -> None:
        """Initializes the class.

        :param camera_conf: CameraConf object with the camera configuration.
        :param queue_size: Size of the queue.
        """
        # Logger
        self.logger = logging.getLogger(f"securitycam.{__name__}")

        # Variables
        self.stopped = False
        self.queue = Queue(maxsize=queue_size)
        self.camera_name = camera_conf.generic_conf.name
        self.camera_address = camera_conf.generic_conf.address

        # Insertion of dummy frame into the queue
        self.dummy_frame = self.__generate_dummy_frame(camera_conf)
        self.queue.put(Frame(self.dummy_frame, self.camera_name))

        self.stream = None

    def start(self) -> None:
        """Starts the thread."""
        self.logger.debug("Instantiating camera object.")
        self.stream = cv2.VideoCapture(self.camera_address)

        self.logger.info("Starting the camera acquisition thread.")
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

    def update(self) -> None:
        """Updates the queue with the frames."""
        while True:
            if self.stopped:
                break

            grabbed, frame = self.stream.read()

            if grabbed:
                if not self.queue.full():
                    self.queue.put(Frame(frame, self.camera_name))
                else:
                    self.logger.warning("Queue full. Dropping frame.")
            else:
                self.logger.info(f"Connection lost on {self.camera_name}. "
                                 f"Retrying in {RECONNECTION_RETRY_DELAY} seconds.")
                self.stream.release()
                self.stream = cv2.VideoCapture(self.camera_address)
                time.sleep(RECONNECTION_RETRY_DELAY)

            time.sleep(SLEEP_TIME_BETWEEN_FRAMES)

    def read(self) -> Frame:
        """Returns the frame from the queue.

        :return: Frame object from queue.
        """
        return self.queue.get()

    def more(self) -> bool:
        """Returns True if there are frames in the queue.

        :return: True if there are frames in the queue.
        """
        return self.queue.qsize() > 0

    def stop(self) -> None:
        """Stops the thread."""
        self.logger.info("Stopping the camera acquisition thread.")
        self.stopped = True
        self.stream.release()

    def __generate_dummy_frame(self, camera_conf: CameraConf) -> np.ndarray:
        """Generates a dummy frame as np.ndarray.

        :param camera_conf: CameraConf object with the camera configuration.
        :return: ndarray with a dummy frame.
        """
        # Text configuration
        font_scale = 1
        thickness = 2
        color = (255, 255, 255)  # White color
        font = cv2.FONT_HERSHEY_COMPLEX

        # Create a black dummy_frame
        dummy_frame = np.zeros((DUMMY_FRAME_HEIGHT, DUMMY_FRAME_WIDTH, 3), dtype="uint8")
        camera_ip = self.__extract_ip_from_address(camera_conf.generic_conf.address)

        # Define the text
        text = f"{camera_conf.generic_conf.name}"
        text_2 = f"@ {camera_ip}"
        text_3 = "Not Available"

        # Get the width and height of the text box
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        (text_width_2, _), _ = cv2.getTextSize(text_2, font, font_scale, thickness)
        (text_width_3, _), _ = cv2.getTextSize(text_3, font, font_scale, thickness)

        # Calculate the center position
        text_x = (dummy_frame.shape[1] - text_width) // 2
        text_x_2 = (dummy_frame.shape[1] - text_width_2) // 2
        text_x_3 = (dummy_frame.shape[1] - text_width_3) // 2
        text_y = (dummy_frame.shape[0] + text_height) // 2

        # Put the text on the dummy_frame
        cv2.putText(dummy_frame, text, (text_x, text_y-40), font, font_scale, color,
                    thickness)
        cv2.putText(dummy_frame, text_2, (text_x_2, text_y), font, font_scale, color,
                    thickness)
        cv2.putText(dummy_frame, text_3, (text_x_3, text_y+40), font, font_scale, color,
                    thickness)

        return dummy_frame

    @staticmethod
    def __extract_ip_from_address(address: str) -> str:
        """Extracts the IP from the address.

        :param address: String with the address.
        :return: String with the IP.
        """
        pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

        # Find all matches in the string
        matches = re.findall(pattern, address)
        return matches[0]
