__author__ = "Eolus"

# Standard libraries
from dataclasses import dataclass, field, asdict
import os
import yaml
import typing
# Third party libraries
# Custom libraries


@dataclass
class GenericConf:
    name: str = field(init=True, repr=True, default="")
    address: str = field(init=True, repr=True, default="")
    store_path: str = field(init=True, repr=True, default="")


@dataclass
class MotionDetector:
    contour_min_area: int = field(init=True, repr=True, default=500)
    threshold_value: int = field(init=True, repr=True, default=35)


@dataclass
class PeopleDetector:
    confidence_threshold: float = field(init=True, repr=True, default=0.8)
    iou_threshold: float = field(init=True, repr=True, default=0.45)


@dataclass
class CameraConf:
    generic_conf: GenericConf = field(init=False, repr=True, default=GenericConf())
    motion_detector_conf: MotionDetector = field(
        init=False,
        repr=True,
        default=MotionDetector()
    )
    people_detector_conf: PeopleDetector = field(
        init=False,
        repr=True,
        default=PeopleDetector()
    )

    def __init__(self, conf_path: str):
        """Initializes the class.

        :param conf_path: String with the path to the configuration file.
        """
        with open(os.path.normpath(conf_path)) as f:
            camera_conf = yaml.load(f, Loader=yaml.FullLoader)

        self.generic_conf = GenericConf(
            camera_conf['generic']['name'],
            camera_conf['generic']['address'],
            camera_conf['generic']['store_path'])
        self.motion_detector_conf = MotionDetector(
            camera_conf['motion_detector']['contour_min_area'],
            camera_conf['motion_detector']['threshold_value'])
        self.people_detector_conf = PeopleDetector(
            camera_conf['people_detector']['confidence_threshold'],
            camera_conf['people_detector']['iou_threshold'])

        self.__type_check()

    def __type_check(self):
        attributes_and_types = typing.get_type_hints(CameraConf)
        current_class_asdict = asdict(self)
        for i in range(len(attributes_and_types)):
            key = list(attributes_and_types.keys())[i]
            if isinstance(attributes_and_types[key], type(current_class_asdict[key])):
                raise TypeError(f"Camera conf {key} incorrect type.")
