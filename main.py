__author__ = "Eolus"

# Standard libraries
import os
import time
# Third party libraries
import cv2
# Custom libraries
from camera.filevideostream import FileVideoStream
from data_classes.cameraconf import CameraConf
from processing.motiondetector import MotionDetector
from interfaces.fileinterface import FileInterface
from data_classes.frame import Frame
from utilities.init_logger import init_logger

# conf_file_pattern = r'^_[A-Za-z\d_ ]*.yaml$'

# Configuration
conf_base_path = r"camera_confs"
conf_filename = "_ipcam_1.yaml"
conf_path = os.path.join(conf_base_path, conf_filename)
camera_conf = CameraConf(conf_path)

filevideostream = FileVideoStream(camera_conf.address)
motiondetector = MotionDetector()
fileinterface = FileInterface(camera_conf.name, camera_conf.store_path)
filevideostream.start()

init_logger(camera_conf.name)

while True:
    tic = time.time()
    frame = filevideostream.read()
    motion_detected, frame_with_detection = motiondetector.detect_motion(frame)
    if motion_detected:
        fileinterface.notify(Frame(frame_with_detection, camera_conf.name))
    toc = time.time() - tic
    print(f"Frame time {toc:.2f} s")
