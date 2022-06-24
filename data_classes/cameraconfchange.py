# Personal Project
__author__ = "Eolus"

# Standard libraries
from dataclasses import dataclass, field
# Third party libraries
# Custom libraries
from data_classes.cameraconfchangeenum import CameraConfChangeEnum
from data_classes.cameraconf import CameraConf
from camera.camerahandlervideo import CameraHandlerVideo


@dataclass
class CameraConfChange:
    conf_path: str = field(init=True, repr=True)
    action: CameraConfChangeEnum = field(init=True, repr=True)
    camera_conf: CameraConf = field(init=False, repr=False)
    camera_handler: CameraHandlerVideo = field(init=False, repr=False)

    def __post_init__(self):
        if self.action != CameraConfChangeEnum.DELETED:
            self.camera_conf = CameraConf().read_from_file(self.conf_path)
