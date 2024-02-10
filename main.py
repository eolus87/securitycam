__author__ = "Eolus"

# Standard libraries
import os
import time
# Third party libraries
# Custom libraries
from camera.filevideostream import FileVideoStream
from data_classes.cameraconf import CameraConf
from processing.motiondetector import MotionDetector
from interfaces.fileinterface import FileInterface
from utilities.init_logger import init_logger
from processing.peopledetector import PeopleDetector

# conf_file_pattern = r'^_[A-Za-z\d_ ]*.yaml$'

# Configuration
conf_base_path = r"camera_confs"
conf_filename = "_ipcam_1.yaml"
conf_path = os.path.join(conf_base_path, conf_filename)
camera_conf = CameraConf(conf_path)

filevideostream = FileVideoStream(camera_conf)
motiondetector = MotionDetector(camera_conf)
peopledetector = PeopleDetector(camera_conf)
fileinterface = FileInterface(camera_conf)
filevideostream.start()

init_logger(camera_conf.generic_conf.name)

while True:
    tic = time.time()
    frame = filevideostream.read()
    motion_detected, frame_with_detection = motiondetector.detect_motion(frame)
    people_detected, frame_with_people_detection = peopledetector.detect_people(frame)
    if motion_detected:
        fileinterface.store(frame_with_detection, "motion")
    if people_detected:
        fileinterface.store(frame_with_people_detection, "people")
    toc = time.time() - tic
    print(f"Frame time {toc:.2f} s")
