import cv2
import time
import pyrealsense2
from realsense_depth import *


dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
count = 0
ret, depth_frame_back, color_frame_back = dc.get_frame()
while True:
    ret, depth_frame, color_frame = dc.get_frame()
    color_crop = color_frame[:,140:460]




    cv2.imshow("Color frame", color_crop)
    key = cv2.waitKey(1)
    if key == 27:
        break
