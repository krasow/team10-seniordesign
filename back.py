import cv2
import pyrealsense2
import numpy as np
import imutils
import time
import lgpio
from realsense_depth import *

dc = DepthCamera()

time.sleep(3)
ret, depth_back, color_back = dc.get_frame()
gray_back = cv2.cvtColor(color_back, cv2.COLOR_BGR2GRAY)[:, 140:460]
depth_back_crop = depth_back[:,140:460]

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    cropped = color_frame[:, 140:460]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("regular",depth_frame_crop)

    gray = cv2.absdiff(gray, gray_back)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1]
    # 100 is a good threshold for low light (windows closed), 130 is good for bright (windows open)
    cv2.imshow("thresh",thresh)
    key = cv2.waitKey(1)
    if key == 27:
        break

