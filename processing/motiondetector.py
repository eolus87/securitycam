__author__ = "Nicolas Gutierrez"


# Standard libraries
import logging
# Third party libraries
import cv2
# Custom libraries

CONTOUR_AREA_THRESHOLD = 500
THRESHOLD_VALUE = 35


class MotionDetector:
    def __init__(self):
        self.logger = logging.getLogger(f"securitycam.{__name__}")
        self.previous_frame = None

    def detect_motion(self, frame):
        motion_detected = False
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
        else:
            frame_delta = cv2.absdiff(self.previous_frame, gray)
            thresh = cv2.threshold(frame_delta, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(
                thresh.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                if cv2.contourArea(contour) > CONTOUR_AREA_THRESHOLD:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.logger.info("Motion detected")
                    motion_detected = True

            self.previous_frame = gray

        return motion_detected, frame
