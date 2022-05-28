# Personal project
__author__ = "Eolus"

# Standard libraries
import cv2
from skimage.metrics import structural_similarity as ssim
import time
import os
import datetime
import numpy as np
# Third party libraries
# Custom libraries


class detectiononSSIM:
    def __init__(self, captureobjectpath, storingpath, imgcounter, windowname):
        # Inputs
        self.captureobjectpath = captureobjectpath
        self.storingpath = storingpath
        self.imgcounter = imgcounter
        self.windowname = windowname

        # Initializations
        self.captureobject = cv2.VideoCapture(captureobjectpath)
        self.ssimvector = np.ones(5)*0.4
        cv2.namedWindow(self.windowname)
        if self.captureobject.isOpened():  # try to get the first frame
            self.rval0, self.frame0 = self.captureobject.read()
            cv2.imshow(self.windowname, self.frame0)
        else:
            self.rval0 = False         

        # Folder creation
        currentdate = datetime.datetime.now()
        self.currentdate = currentdate.strftime("%y%m%d_%H%M%S")
        if not os.path.exists(self.storingpath+self.currentdate[0:6]):
            os.makedirs(self.storingpath+self.currentdate[0:6])
                
    def takepicture(self):
        if self.captureobject.isOpened():  # try to get the first frame
            self.rval0, self.frame0 = self.captureobject.read()
            cv2.imshow(self.windowname, self.frame0)
        else:
            self.rval0 = False
            
    def takeandsavepicture(self):
        if self.captureobject.isOpened():  # try to get the first frame
            self.rval0, self.frame0 = self.captureobject.read()
            cv2.imshow(self.windowname, self.frame0)
            currentdate = datetime.datetime.now()
            self.currentdate = currentdate.strftime("%y%m%d_%H%M%S")
            print("{}-{} - Saving picture {}".format(self.windowname, self.currentdate, self.windowname))
            cv2.imwrite(("{}\\{}.jpg".format(self.storingpath+self.currentdate[0:6], self.currentdate[7:])), self.frame0)
        else:
            self.rval0 = False
        
    def detection(self, threshold):
        # Checking the date
        currentdate = datetime.datetime.now()
        currentdate = currentdate.strftime("%y%m%d_%H%M%S")
        if currentdate[0:6] != self.currentdate:
            self.currentdate    = currentdate
            if not os.path.exists(self.storingpath+self.currentdate[0:6]):
                os.makedirs(self.storingpath+self.currentdate[0:6])
        
        # Checking pictures and measuring SSIM
        self.rval1, self.frame1 = self.captureobject.read()
        self.ssim = ssim(self.frame0, self.frame1,multichannel=True)
        self.frame0 = self.frame1
        print('{0}-{1}: SSIM:{2:.3f}/{3:.3f}'.format(self.windowname,currentdate,self.ssim,np.mean(self.ssimvector)))
        self.ssimvector = np.append(self.ssimvector,self.ssim)
        self.ssimvector = self.ssimvector[1:]
#        print(ssimvector)
        cv2.imshow(self.windowname, self.frame1)
        
        # If we detect something that changes the SSIM we save a picture
        if self.ssim < threshold*np.mean(self.ssimvector):
            for j in range(0, 20):
                currentdate = datetime.datetime.now()
                currentdate = currentdate.strftime("%y%m%d_%H%M%S")
                self.rval1, self.frame1 = self.captureobject.read()
                self.ssim = ssim(self.frame0, self.frame1,multichannel=True)
                print('{0}: SSIM:{1:.3f}/{2:.3f} SAVING TO DISK {3}'.format(currentdate,self.ssim,np.mean(self.ssimvector),j))
                self.ssimvector = np.append(self.ssimvector,self.ssim)
                self.ssimvector = self.ssimvector[1:]
                self.frame0     = self.frame1
                cv2.imwrite(("{}\\{}_DETECTION_{}.jpg".format(self.storingpath+self.currentdate[0:6],currentdate[7:],j)), self.frame1)
                cv2.imshow(self.windowname, self.frame1)
                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    break
                time.sleep(0.25)
