__author__ = "Eolus"

# Standard libraries
import logging
# Third party libraries
import torch
# Custom libraries
from data_classes.frame import Frame

CONFIDENCE_THRESHOLD = 0.8  # confidence threshold (0-1)
IOU_THRESHOLD = 0.45  # NMS IoU threshold (0-1)
CLASSES = [0]  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs


class PeopleDetector:
    def __init__(self) -> None:
        self.logger = logging.getLogger(f"securitycam.{__name__}")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.conf = CONFIDENCE_THRESHOLD
        self.model.iou = IOU_THRESHOLD
        self.model.classes = CLASSES

    def detect_people(self, frame: Frame) -> (bool, Frame):
        # Calculation
        results = self.model(frame.values)

        # Results heuristics
        if len(results.pred[0]) > 0:  # If people are detected
            self.logger.info("People detected")
            results.render()
            people_detected = True
            frame_to_return = Frame(results.ims[0], frame.cam_name)
        else:
            people_detected = False
            frame_to_return = frame

        return people_detected, frame_to_return
