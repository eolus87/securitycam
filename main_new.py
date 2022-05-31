# Personal project
__author__ = "Eolus"

# Standard libraries
import os
import yaml
# Third party libraries
# Custom libraries
from camera.camerahandlervideo import CameraHandlerVideo


cam_name = "_ipcam_1"

with open(os.path.join("camera_confs", f"{cam_name}.yaml")) as f:
    camera_details = yaml.load(f, Loader=yaml.FullLoader)

camera_handler = CameraHandlerVideo(camera_details['address'], camera_details['name'], 30, True)

camera_handler.run()
