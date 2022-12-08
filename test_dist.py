import cv2
import time
import pyrealsense2
from realsense_depth import *

point = (310,390)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)
count = 0
ret, depth_frame_back, color_frame_back = dc.get_frame()
#depth_back_crop = depth_frame_back[:,140:460]
while True:
    ret, depth_frame, color_frame = dc.get_frame()
    #color_crop = color_frame[:,140:460]
    #depth_crop = depth_frame[:,140:460]
    #time.sleep(.5)
    norm = cv2.absdiff(depth_frame_back,depth_frame)
    # Show distance for a specific point
    cv2.circle(color_frame, (point[0],point[1]), 4, (0, 0, 255))
    distance = norm[point[1], point[0]]/10

    '''
    max_ = -1
    for i in range(-5,5):
        for j in range(-5,5):
            if (norm[point[1]+i,point[0]+j] > max_):
                max_ = norm[point[1]+i,point[0]+j]

    if (max_ > 4 and point[0] > 140 and point[0] < 460):
        print(f"stacked bag detected #{count}\n")
        count += 1
    '''



    cv2.putText(color_frame, "{}cm".format(distance), (281, 56), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    #print(f"absolute diff = {distance}\n")

    #cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
