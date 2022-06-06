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

# %% User configuration
cam_name = "_ipcam_1"

# %% Initialization and configuration
pictures_queue = queue.Queue()

with open(os.path.join("camera_confs", f"{cam_name}.yaml")) as f:
    camera_details = yaml.load(f, Loader=yaml.FullLoader)

# %% 

camera_handler = CameraHandlerVideo(camera_details['address'], camera_details['name'], 30, True, pictures_queue)

threading.Thread(target=camera_handler.run, daemon=True).start()

try:
    while True:
        print(f"{datetime.datetime.now().strftime('%y%m%d_%H%M%S')} Waiting for a picture")
        picture = pictures_queue.get()
        print(f"{datetime.datetime.now().strftime('%y%m%d_%H%M%S')} Picture detected")
        
        time.sleep(0.5)
    
except KeyboardInterrupt:
    print("Keyboard interrup detected, closing the connection to cam.")
    camera_handler.keep_running = False
    time.sleep(5)

