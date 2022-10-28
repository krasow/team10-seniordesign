from turtle import color
import cv2
import pyrealsense2
import webcolors as wc
from realsense_depth import *
import sys 
point = (400, 300)

# list of dictionary to store all the detected bean bags
objects = [] 
board_location = [] # all four points but first index is bottom left of the board going clockwise


def determine_board_location(frame):
    # need to detect the board in the frame


def getObjectScore(new):
    if checkBoardLocation(new):
        if sys.interupt(34):
            new["score"] = 3
        else:
            new["score"] = 1
    
            


def checkBoardLocation(new):
    #figure out if its a new centroid using surrounding values
    if new["point"][0] >  board_location[0][0] and new["point"][1] > board_location[0][1]:
        if  new["point"][0] <  board_location[2][0] and new["point"][1] < board_location[2][1]:
            return True
    else:
        return False


def detect_object(new):
    # append new centroid to datastruct if different
    for obj in objects:
        # if old object equal new id
        if obj["id"] == new["id"]
            return 1

    # check on board
    new_bag = checkBoardLocation(new)
    if new_bag:
        new.update({"score" : getObjectScore(new)})
        objects.append(new)
        

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)
    RGB = np.flip(color_frame[y][x])
    if (RGB[0] > 150 and RGB[1] < 100 and RGB[2] < 100):
        color = "red"
    else:
        color = "blue"
    # we need to use opencv to gain centroids
    new = {"point": point, "color": color, "id": centroid.id} 
    detect_object(new)


#main

# Initialize Camera Intel Realsense
dc = DepthCamera()


# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

# determine board location
board_location = determine_board_location(dc.get_frame())
print("board location found")


while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show distance for a specific point
    #cv2.circle(color_frame, point, 4, (0, 0, 255))
    distance = depth_frame[point[1], point[0]]

    cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    
    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
