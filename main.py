__author__ = "Eolus"

# Standard libraries
import os
import time
import glob
from multiprocessing import Process, Manager
# Third party libraries
import cv2
# Custom libraries
from data_classes.cameraconf import CameraConf
from workflow.orchestrator import Orchestrator

# Constants
DEBUGGING = True
CONFIGURATION_PATH = "camera_confs"
CONFIGURATION_FORMAT = "yaml"
TIME_BETWEEN_PROCESS_INITILIZATION = 1  # s
TIME_BETWEEN_PROCESS_START = 1  # s

print("Working with camera configurations")
list_of_configurations = glob.glob(
    os.path.join(CONFIGURATION_PATH,
                 f"*.{CONFIGURATION_FORMAT}"
                 )
    )
list_of_configuration_objects = []
for conf_path in list_of_configurations:
    try:
        list_of_configuration_objects.append(CameraConf(conf_path))
    except Exception as e:
        print(f"An error occurred: {e}")

print("Starting the orchestrators")
list_of_processes = []
try:
    with Manager() as manager:
        shared_dict = manager.dict()
        print("Launching the processes.")
        for conf_object in list_of_configuration_objects:
            p = Process(target=Orchestrator().start, args=(conf_object, shared_dict,))
            p.start()
            list_of_processes.append(p)
            time.sleep(TIME_BETWEEN_PROCESS_START)

        print("Starting the visualization.")
        while True:
            if DEBUGGING:
                for conf_object in list_of_configuration_objects:
                    try:
                        frame = shared_dict[conf_object.generic_conf.name]
                        if frame is not None:
                            cv2.imshow(conf_object.generic_conf.name, frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    except Exception as e:
                        print(f"An error occurred: {e}")

            time.sleep(0.15)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if DEBUGGING:
        cv2.destroyAllWindows()
    for p in list_of_processes:
        p.join()
