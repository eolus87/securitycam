# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 23:04:58 2019

@author: Eolus
"""
#%% Needed Libraries
import cv2
#from skimage.metrics import structural_similarity as ssim
from skimage.measure import compare_ssim as ssim
import time
import os
import datetime
import numpy as np

#%% Parameters
path_1      = "E:\\OneDrive\\camsurveillance\\laptop\\"
img_counter = 60

#%% Variables initialization
cv2.namedWindow("preview")
vc      = cv2.VideoCapture(0)

stream = cv2.VideoCapture('http://admin:1234@192.168.0.79:80/video/mjpg.cgi') 
cv2.namedWindow("IPcam")

if vc.isOpened(): # try to get the first frame
    rval, frame0 = vc.read()
else:
    rval = False

if stream.isOpened():
    r, f0 = stream.read()
else:
    r = False

i = 0

ssimvector = np.ones(5)*0.4
ssimvector2 = np.ones(5)*0.4

currentdate = datetime.datetime.now()
currentdate = currentdate.strftime("%y%m%d_%H%M%S")
path_2      = currentdate
if not os.path.exists(path_1+path_2[0:6]):
    os.makedirs(path_1+path_2[0:6])

#%% Infinite loop for doing the detection
while rval:
    #1 - Folders sorting
    currentdate = datetime.datetime.now()
    currentdate = currentdate.strftime("%y%m%d_%H%M%S")
    if currentdate[0:6] != path_2:
        path_2      = currentdate[0:6]
        if not os.path.exists(path_1+path_2):
            os.makedirs(path_1+path_2)
    
    # Reading picture and detection logic from webcam
    rval, frame1 = vc.read()
    ssim_01 = ssim(frame0, frame1,multichannel=True)
    frame0 = frame1
    print('{0}: SSIM:{1:.3f}/{2:.3f}'.format(currentdate,ssim_01,np.mean(ssimvector)))
    ssimvector = np.append(ssimvector,ssim_01)
    ssimvector = ssimvector[1:]    
    print(ssimvector)
    cv2.imshow("preview", frame1)
    
    # Reading picture and detection logic from IP cam
    r, f1 = stream.read()
    ssim_11 = ssim(f0,f1,multichannel=True)
    f0 = f1
    print('{0}: SSIM:{1:.3f}/{2:.3f}'.format(currentdate,ssim_11,np.mean(ssimvector2)))
    ssimvector2 = np.append(ssimvector2,ssim_11)
    ssimvector2 = ssimvector2[1:]    
    print(ssimvector2)
    cv2.imshow("IPcam",f1)
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    
    i = i+1
    if i > 300:
        cv2.imwrite(("{}\\{}.jpg".format(path_1+path_2,currentdate[7:])), frame1)
        i = 0    
    
    if ssim_01 < 0.95*np.mean(ssimvector):
        for j in range(0,20):
            currentdate = datetime.datetime.now()
            currentdate = currentdate.strftime("%y%m%d_%H%M%S")
            rval, frame1 = vc.read()
            ssim_01 = ssim(frame0, frame1,multichannel=True)
            print('{0}: SSIM:{1:.3f}/{2:.3f} SAVING TO DISK {3}'.format(currentdate,ssim_01,np.mean(ssimvector),j))
            ssimvector = np.append(ssimvector,ssim_01)
            ssimvector = ssimvector[1:]
            frame0 = frame1
            cv2.imwrite(("{}\\{}_DETECTION_{}.jpg".format(path_1+path_2,currentdate[7:],j)), frame1)
            cv2.imshow("preview", frame1)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            time.sleep(1)
            
    if ssim_11 < 0.95*np.mean(ssimvector2):
        for j in range(0,20):
            currentdate = datetime.datetime.now()
            currentdate = currentdate.strftime("%y%m%d_%H%M%S")
            r, f1 = stream.read()
            ssim_11 = ssim(f0, f1,multichannel=True)
            print('{0}: SSIM:{1:.3f}/{2:.3f} SAVING TO DISK {3}'.format(currentdate,ssim_11,np.mean(ssimvector2),j))
            ssimvector2 = np.append(ssimvector2,ssim_11)
            ssimvector2 = ssimvector2[1:]
            f0 = f1
            cv2.imwrite(("{}\\{}_DETECTION_{}.jpg".format(path_1+path_2,currentdate[7:],j)), f1)
            cv2.imshow("IPCam", f1)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            time.sleep(1)

    time.sleep(1)       
cv2.destroyWindow("preview")
cv2.destroyWindow("IPCam")