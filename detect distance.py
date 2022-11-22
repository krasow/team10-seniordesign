# detect distance.py
# ECE-4960 : Senior Design II
# Automated Cornhole
# Jason Baer, Aaron Bruner, David Krasowska, Ross Snead
# References - https://pysource.com/2021/03/11/distance-detection-with-depth-camera-intel-realsense-d435i/

import cv2
import pyrealsense2
import numpy as np
import imutils
from realsense_depth import *

# Initialize Camera Intel Realsense
dc = DepthCamera()

def getColor(x, y, image):
    RGB = np.flip(image[y][x])
    if (RGB[0] > RGB[1] and RGB[0] > RGB[2]):
        return "RED"
    elif (RGB[2] > RGB[0] and RGB[1] < RGB[2]):
        return "BLUE"
    else:
        return ""

while True:
    ret, depth_frame, color_frame = dc.get_frame()

    cropped = color_frame[20:470, 140:460]

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1] # 100 is a good threshold for low light (windows closed), 130 is good for bright (windows open)

    contoursArr = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contoursArr = imutils.grab_contours(contoursArr)

    for contour in contoursArr:
        # compute the center of the contour
        M = cv2.moments(contour)
        if (cv2.contourArea(contour) > 500 and cv2.contourArea(contour) < 5000):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # draw the contour and center of the shape on the color_frame
            cv2.drawContours(cropped, [contour], -1, (0, 255, 0), 2)
            color = getColor(cX, cY, cropped)

            #cv2.putText(cropped, f"center {cv2.contourArea(contour)}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #cv2.putText(cropped, f"color {color}",                     (cX - 40, cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Color frame", cropped)
    cv2.imshow("Threshold Image",thresh)

    key = cv2.waitKey(1)
    if key == 27:
        break


'''
Score Handler

* Loop over redBags & blueBags array and determine if they have changed since last time
    -> If array count increases then increase score using the following logic:
        * Bag count has decreased and light barrier interrupt has been triggered
            * Increase bagColorScore by 3 for x number of bags that have left the array
        * Bag count has decreased and light barrier has not been triggered
            * Decrease bagColorScore by 1 for x number of bags that have left the array
    -> If array count decreases then check if light barrier has been triggered
        * Light Barrier has not been broken: decrease bagColorScore by x number of bags
        * Light Barrier has been broken: Check difference in each team's bag count and handle using standard logic
'''