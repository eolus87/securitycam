# Personal project
__author__ = "Eolus"

# Standard libraries
import time
import cv2
import threading
# Third party libraries
# Custom libraries
from processing import detectiononSSIM

windowname = "IPcam"
captureobjectpath = 'http://admin:1234@192.168.0.79:80/video/mjpg.cgi'
storingpath = "E:\\OneDrive\\camsurveillance\\Dlink\\"
imgcounter = 60

windowname_2 = "Laptop"
captureobjectpath_2 = 0
storingpath_2 = "E:\\OneDrive\\camsurveillance\\laptop\\"
imgcounter_2 = 60


def continuousmonitoring(cameraobject, windowname, intervaltime, saveeveryn, threshold):
    i = 0
#    threshold = 0.996
    while True:
        # Check the key to break the loop
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            cv2.destroyWindow(windowname)
            break
        
        # Flag to save a picture 
        i = i+1
#        print(i)
        if i > saveeveryn:
            cameraobject.takeandsavepicture()
            i = 0   
        
        cameraobject.detection(threshold)
        
        time.sleep(intervaltime)



camera = detectiononSSIM.detectiononSSIM(captureobjectpath,
                                         storingpath,
                                         imgcounter,
                                         windowname)

# camera2 = detectiononSSIM.detectiononSSIM(captureobjectpath_2,
#                                          storingpath_2,
#                                          imgcounter_2,
#                                          windowname_2)


#continuousmonitoring(camera,windowname,0.5,10)

x = threading.Thread(target=continuousmonitoring, args=(camera, windowname, 0.5, 600, 0.996))
x.start()

# x2 = threading.Thread(target=continuousmonitoring, args=(camera2, windowname_2, 0.5, 600, 0.95))
# x2.start()

#while True:
#    # Check the key to break the loop
#    key = cv2.waitKey(20)
#    if key == 27: # exit on ESC
#        x.join()
#        x2.join()
#        break
#    time.sleep(0.5)