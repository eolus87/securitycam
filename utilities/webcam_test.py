# Personal project
__author__ = "Eolus"

# Standard libraries
import os
import yaml
import time
import cv2
# Thirdparty libraries
# Custom libraries


#%% Input variables

cam_name = "_ipcam_1"


# %% Load the configuration of the cam

with open(os.path.join("..", "camera_confs", f"{cam_name}.yaml")) as f:
    camera_details = yaml.load(f, Loader=yaml.FullLoader)

# %% Initialize the camera

cam_stream = cv2.VideoCapture(camera_details['address']) 
cv2.namedWindow(camera_details['name'])

if cam_stream.isOpened():
    rval, f0 = cam_stream.read()
else:
    rval = False


#%% Loop until ESC is pressed
while rval:   
    # Reading picture and detection logic from IP cam
    rval, f1 = cam_stream.read()

    cv2.imshow(camera_details['name'], f1)
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    
    time.sleep(0.01)       
cv2.destroyWindow(camera_details['name'])
