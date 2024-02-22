__author__ = "Eolus"

# Standard libraries
import logging
# Third party libraries
import torch
# Custom libraries
from data_classes.frame import Frame
from data_classes.cameraconf import CameraConf

# (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs
CLASSES = [0]


class PeopleDetector:
    """This class has been developed using the code in the following website:
    https://news.machinelearning.sg/posts/object_detection_with_yolov5/
    Credits to Eugene."""
    def __init__(self, camera_conf: CameraConf) -> None:
        """Initializes the class.

        :param camera_conf: CameraConf object with the camera configuration.
        """
        self.logger = logging.getLogger(f"securitycam.{__name__}")

        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n6', pretrained=True)
        self.model.conf = camera_conf.people_detector_conf.confidence_threshold
        self.model.iou = camera_conf.people_detector_conf.iou_threshold
        self.model.classes = CLASSES

    def detect_people(self, frame: Frame) -> (bool, Frame):
        """Detects people in the frame.

        :param frame: Frame object with the frame to analyze.
        :return: Tuple with a boolean indicating if people were detected
        and a Frame object with the detection.
        """
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
