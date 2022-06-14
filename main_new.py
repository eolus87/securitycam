# Personal project
__author__ = "Eolus"

# Standard libraries
import os
import yaml
import queue
import threading
import time
import datetime
# Third party libraries
# Custom libraries
from camera.camerahandlervideo import CameraHandlerVideo
from interfaces.fileinterface import FileInterface

# %% User configuration
cam_name_1 = "_ipcam_1"
cam_name_2 = "_ipcam_nexus_ipwebcam"

# %% Initialization and configuration
pictures_queue = queue.Queue()

with open(os.path.join("camera_confs", f"{cam_name_1}.yaml")) as f:
    camera_details_1 = yaml.load(f, Loader=yaml.FullLoader)

with open(os.path.join("camera_confs", f"{cam_name_2}.yaml")) as f:
    camera_details_2 = yaml.load(f, Loader=yaml.FullLoader)

# %% Initialization of classes

camera_handler_1 = CameraHandlerVideo(camera_details_1['address'], 
                                      camera_details_1['name'], 
                                      camera_details_1['frames_per_minute'], 
                                      True, pictures_queue)
picture_file_interface_1 = FileInterface(camera_details_1['name'], 
                                         camera_details_1['store_path'])

camera_handler_2 = CameraHandlerVideo(camera_details_2['address'], 
                                      camera_details_2['name'], 
                                      camera_details_2['frames_per_minute'], 
                                      True, pictures_queue)
picture_file_interface_2 = FileInterface(camera_details_2['name'], 
                                         camera_details_2['store_path'])


# %% Thread creation and While Loop

threading.Thread(target=camera_handler_1.run, daemon=True).start()
threading.Thread(target=camera_handler_2.run, daemon=True).start()

try:
    while True:
        print(f"{datetime.datetime.now().strftime('%y%m%d_%H%M%S')} Waiting for a picture")
        new_frame = pictures_queue.get()
        print(f"{datetime.datetime.now().strftime('%y%m%d_%H%M%S')} Picture detected")
        picture_file_interface_1.store(new_frame)
        picture_file_interface_2.store(new_frame)
        time.sleep(0.02)
    
except KeyboardInterrupt:
    print("Keyboard interrup detected, closing the connection to cam.")
    camera_handler_1.keep_running = False
    camera_handler_2.keep_running = False
    time.sleep(5)

