# code from Sergio Canu (PySource) https://pysource.com/2021/03/11/distance-detection-with-depth-camera-intel-realsense-d435i/

from turtle import color
import cv2
import pyrealsense2
import numpy as np
import pandas as pd
import time
import argparse
import imutils
from realsense_depth import *

point = (400, 300)


def show_distance(event, x, y, args, params):
    global point
    point = (x, y)
    RGB = np.flip(color_frame[y][x])
    if (RGB[0] > 125 and RGB[1] < 100 and RGB[2] < 100):
        print(f"RED -> {RGB}")
    elif (RGB[0] < 50 and RGB[1] < 100 and RGB[2] > 75):
        print(f"BLUE -> {RGB}")
    elif (RGB[0] > 100 and RGB[1] > 80 and RGB[2] > 80):
        if (RGB[0] > RGB[2]):
            print(f"Board -> {RGB}")
        else:
            print(f"Background -> {RGB}")
    else:
        print(f"Background -> {RGB}")

    

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()


    # for y in range(0,480,1):
    #     for x in range(0,640,1):
    #         #if (y > 20 and y < 470 and x > 140 and x < 460):
    #         RGB = color_frame[y][x]
    #         #distance = depth_frame[x, y]
    #         if (RGB[2] > 125 and RGB[1] < 100 and RGB[0] < 100):
    #             #cv2.putText(color_frame, "{}mm".format(distance), (y, x - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    #             color_frame[y][x] = [0,0,255]
    #         elif (RGB[2] < 50 and RGB[1] < 100 and RGB[0] > 75):
    #             color_frame[y][x] = [255,0,0]
    #             #cv2.putText(color_frame, "{}mm".format(distance), (y, x - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    #         elif (RGB[2] > 120 and RGB[1] > 100 and RGB[0] > 100):
    #             if (RGB[2] > RGB[0]):
    #                 color_frame[y][x] = [50,50,50]
    #             else:
    #                 color_frame[y][x] = [0,0,0]
    #         else:
    #             color_frame[y][x] = [0,0,0]
    #         #else:
    #             #color_frame[y][x] = [255,255,255]
    # blur = cv2.GaussianBlur(color_frame,(3,3),10)

    # useless variables for demo, allow for finding 2 of each bag
    red_flag1 = 0
    red_flag2 = 0
    blue_flag1 = 0
    blue_flag2 = 0

    # blur to try and get rid of noise on floor
    blur = cv2.GaussianBlur(color_frame,(7,7),10)

    # loop all pixels in image
    for y in range(0,480,1):
        for x in range(0,640,1):
            RGB = blur[y][x]
            # red bags
            if (RGB[2] > 125 and RGB[1] < 100 and RGB[0] < 100):
                if (y > 100 and red_flag1 == 0):
                    cv2.putText(blur, "RED", (x-20, y+20), cv2.FONT_HERSHEY_DUPLEX, .5, (255, 255, 255), 1)
                    red_flag1 = 1
                if (y > 200 and red_flag2 == 0):
                    cv2.putText(blur, "RED", (x+20, y+20), cv2.FONT_HERSHEY_DUPLEX, .5, (255, 255, 255), 1)
                    red_flag2 = 1
                blur[y][x] = [0,0,255]
                #blue bags
            elif (RGB[2] < 50 and RGB[1] < 100 and RGB[0] > 75):
                if (y > 100 and blue_flag1 == 0):
                    cv2.putText(blur, "BLUE", (x-20, y+20), cv2.FONT_HERSHEY_DUPLEX, .5, (255, 255, 255), 1)
                    blue_flag1 = 1
                if (y > 200 and blue_flag2 == 0 and blue_flag1 == 1):
                    cv2.putText(blur, "BLUE", (x-20, y+20), cv2.FONT_HERSHEY_DUPLEX, .5, (255, 255, 255), 1)
                    blue_flag2 = 1
                blur[y][x] = [255,0,0]
                #cv2.putText(blur, "{}mm".format(distance), (y, x - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
            elif (RGB[2] > 120 and RGB[1] > 100 and RGB[0] > 100):
                if(RGB[2] > 150 and RGB[1] > 200 and RGB[0] > 240):
                    blur[y][x] = [0,255,0]
                elif (RGB[2] > RGB[0]):
                    blur[y][x] = [50,50,50]  #board
                else:
                    blur[y][x] = [0,0,0]  #background
            else:
                blur[y][x] = [0,0,0]
            #else:
                #color_frame[y][x] = [255,255,255]


    

    # the original code for contours, as it is right now it just puts the 
    # contour as the border of the image instead of getting the bags

    # cropped = color_frame[20:470, 140:460]

    # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	#     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # for c in cnts:
    #     # compute the center of the contour
    #     M = cv2.moments(c)
    #     # if (M["m00"] == 0):
    #     #     M["m00"] = 1
    #     if cv2.contourArea(c) > 1:
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         # draw the contour and center of the shape on the color_frame
    #         cv2.drawContours(cropped, [c], -1, (0, 255, 0), 2)
    #         cv2.circle(cropped, (cX, cY), 7, (255, 255, 255), -1)
    #         cv2.putText(cropped, "center", (cX - 20, cY - 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #     #show the color_frame




    # Show distance for a specific point
    #cv2.circle(color_frame, point, 4, (0, 0, 255))
    #distance = depth_frame[point[1], point[0]]

    #cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

    #cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", blur)
    key = cv2.waitKey(1)
    if key == 27:
        break

    # since the code right now is a double nested for loop, I added a sleep to make sure there are no issues with 
    # computation time
    time.sleep(5) 
