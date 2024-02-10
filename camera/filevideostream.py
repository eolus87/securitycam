__author__ = "Eolus"

# Standard libraries
from threading import Thread
from queue import Queue
import logging
import time
# Third party libraries
import cv2
# Custom libraries

CONNECTION_RETRY_DELAY = 60  # s
FRAME_QUEUE_SIZE = 128


class FileVideoStream:
    """This class has been taken from the pyimagesearch blog!
    It is a class that allows to read a video file in a different thread. """
    def __init__(self, cam_address: str, queue_size: int = FRAME_QUEUE_SIZE):
        self.logger = logging.getLogger(f"securitycam.{__name__}")
        self.stopped = False
        self.queue = Queue(maxsize=queue_size)

        self.logger.debug("Instantiating camera object.")
        self.stream = cv2.VideoCapture(cam_address)

    def start(self):
        """Starts the thread."""
        self.logger.info("Starting the camera acquisition thread.")
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

    def update(self):
        """Updates the queue with the frames."""
        while True:
            if self.stopped:
                return

            if self.stream.isOpened():
                grabbed, frame = self.stream.read()
                if not grabbed:
                    self.logger.info(f"Connection lost. "
                                     f"Retrying in {CONNECTION_RETRY_DELAY} seconds.")
                    time.sleep(CONNECTION_RETRY_DELAY)
                else:
                    if not self.queue.full():
                        self.queue.put(frame)
                    else:
                        self.logger.warning("Queue full. Dropping frame.")

    def read(self):
        """Returns the frame from the queue."""
        return self.queue.get()

    def more(self):
        """Returns True if there are frames in the queue."""
        return self.queue.qsize() > 0

    def stop(self):
        """Stops the thread."""
        self.logger.info("Stopping the camera acquisition thread.")
        self.stopped = True
        self.stream.release()
