# detect distance.py
# ECE-4960 : Senior Design II
# Automated Cornhole
# Jason Baer, Aaron Bruner, David Krasowska, Ross Snead
# References - https://pysource.com/2021/03/11/distance-detection-with-depth-camera-intel-realsense-d435i/

import cv2
import pyrealsense2
import numpy as np
import imutils
import time
import lgpio
from realsense_depth import *

# Setup everything
# Initialize Camera Intel Realsense
dc = DepthCamera()
# Initialize GPIO pin for laser sensor
laser = 4
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(h, laser)
blueScore = 0
redScore = 0
redInningScore = 0
blueInningScore = 0
redTotal = 0
blueTotal = 0
over = 0



def getColor(x, y, image):
    RGB = np.flip(image[y][x])
    if (RGB[0] > RGB[1] and RGB[0] > RGB[2] and RGB[0] > 80):
        return "RED"
    elif (RGB[2] > RGB[0] and RGB[1] < RGB[2] and RGB[2] > 70):
        return "BLUE"
    else:
        return ""
        
        
# check if a black square is on the board signifying the inning is over
def endInning(x, y, image):
    RGB = np.flip(image[y][x])
    if (RGB[0] < 50 and RGB[2] < 50 and RGB[2] < 50):
        return 1
    else: return 0


redArray = []
blueArray = []
redArrayPrev = []
blueArrayPrev = []
LASER = 0
sinkColor = "none"

time.sleep(3)
ret, depth_back, color_back = dc.get_frame()
gray_back = cv2.cvtColor(color_back, cv2.COLOR_BGR2GRAY)[20:470, 140:460]


while True:
    redArrayPrev = redArray.copy()
    blueArrayPrev = blueArray.copy()
    redArray = []
    blueArray = []

    ret, depth_frame, color_frame = dc.get_frame()
    cropped = color_frame[20:470, 140:460]
    depth = depth_frame[20:470, 140:460]  
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    gray = cv2.absdiff(gray, gray_back)


    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1] # 100 is a good threshold for low light (windows closed), 130 is good for bright (windows open)
    
    contoursArr = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contoursArr = imutils.grab_contours(contoursArr)

    for contour in contoursArr:
        # compute the center of the contour
        if (over == 1):
            
            break
        M = cv2.moments(contour)
        if (cv2.contourArea(contour) > 200 and cv2.contourArea(contour) < 8000):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # draw the contour and center of the shape on the color_frame
            color = getColor(cX, cY, cropped)
            # check for black square
            over = endInning(cX, cY, cropped)
            if (over == 1):
                cv2.drawContours(cropped, [contour], -1, (0, 255, 0), 2)
                if (blueScore > redScore):
                    blueInningScore = blueScore - redScore
                    redInningScore = 0
                elif (redScore > blueScore):
                    redInningScore = redScore - blueScore
                    blueInningScore = 0
                else:
                    redInningScore = blueInningScore = 0
                redTotal += redInningScore
                blueTotal += blueInningScore
                redInningScore = blueInningScore = 0
                break
            # update blue and red arrays for each side
            if color == "BLUE":
                cv2.drawContours(cropped, [contour], -1, (0, 255, 0), 2)
                blueArray.append([cX, cY])
            elif color == "RED":
                cv2.drawContours(cropped, [contour], -1, (0, 255, 0), 2)
                redArray.append([cX, cY])
            else:
                pass
    while(len(contoursArr) != 0 and over == 1):
        ret, depth_frame, color_frame = dc.get_frame()
        cropped = color_frame[20:470, 140:460]
        depth = depth_frame[20:470, 140:460]  
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        gray = cv2.absdiff(gray, gray_back)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1] 
        contoursArr = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contoursArr = imutils.grab_contours(contoursArr)
        print(f"\n\ntotal score\n\n\t\tred : {redTotal}\n\t\tblue: {blueTotal}\n")
        
    if (len(contoursArr) == 0 and over == 1):
        #print(f"\n\ntotal score\n\n\t\tred: {redTotal}\n\t\tblue{blueTotal}\n")
        over = 0
        redScore = blueScore = 0
        redInningScore = blueInningScore = 0
        redArray = []
        blueArray = []
        redArrayPrev = []
        blueArrayPrev = []
        #exit()
        
    if (redTotal > 6):
        print("\n\nRED WINS\n\n")
        exit()

        
    
        
            

            #cv2.putText(cropped, f"center {cv2.contourArea(contour)}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #cv2.putText(cropped, f"color {color}",                     (cX - 40, cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
   

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


    # update blue score
    if len(blueArray) > len(blueArrayPrev):
        bags = len(blueArray) - len(blueArrayPrev) 
        blueScore += 1*bags 
    elif len(blueArray) < len(blueArrayPrev) and LASER:
        bags = len(blueArrayPrev) - len(blueArray)
        #print("\nsink\n")
        #print(f"bags = {bags}\n")
        blueScore += -1*bags
        blueScore += 3*bags
    elif len(blueArray) < len(blueArrayPrev) and not LASER:
        bags = len(blueArrayPrev) - len(blueArray)
        blueScore += -1*bags
    else:
        pass

    # update red score
    if len(redArray) > len(redArrayPrev):
        bags = len(redArray) - len(redArrayPrev)
        redScore += 1*bags
    elif len(redArray) < len(redArrayPrev) and LASER:
        bags = len(redArrayPrev) - len(redArray)
        redScore += -1*bags
        redScore += 3*bags
    elif len(redArray) < len(redArrayPrev) and not LASER:
        bags = len(redArrayPrev) - len(redArray)
        redScore += -1*bags
    else:
        pass
        
       


    cv2.imshow("Color frame", cropped)
    cv2.imshow("Threshold Image",thresh)
    print(f'Red: {redScore} L: {len(redArray)}')
    print(f'Blue: {blueScore} L: {len(blueArray)}')
    print(f"laser = {LASER}")
    
    



   # if laser is detected
    LASER = 0
    if(lgpio.gpio_read(h, laser)):
        LASER = 1
        time.sleep(0.05)
        # we need to sample multiple spots within the hole
        # since the bag might not go perfectly in the center
        sinkColor = getColor(150,350,cropped)
        if (sinkColor == ""):
            sinkColor = getColor(180,350,cropped)
        if (sinkColor == ""):
            sinkColor = getColor(130,350,cropped)
        if (sinkColor == ""):
            sinkColor = getColor(160,380,cropped)
        print(sinkColor)

        #break
    key = cv2.waitKey(1)
    if key == 27:
        break
