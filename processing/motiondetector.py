__author__ = "Eolus"

# Standard libraries
import logging
# Third party libraries
import cv2
# Custom libraries
from data_classes.frame import Frame
from data_classes.cameraconf import CameraConf


class MotionDetector:
    """This class is used to detect motion in the frames."""
    def __init__(self, camera_conf: CameraConf) -> None:
        """Initializes the class.

        :param camera_conf: CameraConf object with the camera configuration.
        """
        self.logger = logging.getLogger(f"securitycam.{__name__}")

        self.contour_area_threshold = \
            camera_conf.motion_detector_conf.contour_min_area
        self.threshold_value = camera_conf.motion_detector_conf.threshold_value
        self.previous_frame = None

    def detect_motion(self, frame: Frame) -> (bool, Frame):
        """Detects motion in the frame.

        :param frame: Frame object with the frame to analyze.
        :return: Tuple with a boolean indicating if motion was detected
        and a Frame object with the detection.
        """
        motion_detected = False
        gray = cv2.cvtColor(frame.values, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
        else:
            frame_delta = cv2.absdiff(self.previous_frame, gray)
            thresh = cv2.threshold(
                frame_delta,
                self.threshold_value,
                255,
                cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(
                thresh.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                if cv2.contourArea(contour) > self.contour_area_threshold:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame.values, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.logger.info("Motion detected")
                    motion_detected = True

            self.previous_frame = gray

        return motion_detected, Frame(frame.values, frame.cam_name)
