# tkinter : python3 -m pip install tk
# pynput  : puthon3 -m pip install pynput

from pynput.keyboard import Key, Controller
from tkinter import *
import tkinter
from tkinter import messagebox
import cv2
import pyrealsense2
import numpy as np
import imutils
import time
import lgpio
from realsense_depth import *

#####################################################################################################
#                           Setup GUI and display initial score                                     #
#####################################################################################################

# Initialize global variables for score
global scoreBLUE, scoreRED; scoreBLUE = scoreRED = 0
global MAX_SCORE, MIN_SCORE; MAX_SCORE = 21; MIN_SCORE = 0
global num; num = 0

dc = DepthCamera()

def getColor(x, y, image):
    RGB = np.flip(image[y][x])
    if (RGB[0] > RGB[1] and RGB[0] > RGB[2] and RGB[0] > 80):
        return "RED"
    elif (RGB[2] > RGB[0] and RGB[1] < RGB[2] and RGB[2] > 70):
        return "BLUE"
    else:
        return ""

# Create instance of keyboard so we can simulate key presses
keyboard = Controller()

# Setup screen with size and background image
GUI = Tk()
GUI.configure(bg='black')
GUI.title("CORNHOLE SCOREBOARD")
GUI.geometry('800x480')
bg = PhotoImage(file = "scoreboard_background.png")
backgroundImage = Label(GUI, image = bg)
backgroundImage.place(x = 0, y = 0)

# Create the blue player's score label
BLUE_SCORE = IntVar()
BLUE_SCORE.set(scoreBLUE)
BLUE_SCORE_LABEL = Label(GUI, textvariable=BLUE_SCORE, font=("times", 250, 'bold'), bg="blue", justify=CENTER)
BLUE_SCORE_LABEL.pack()
BLUE_SCORE_LABEL.place(relx=0.25, rely=0.5, anchor='center')

# Create the red player's score label
RED_SCORE = IntVar()
RED_SCORE.set(scoreRED)
RED_SCORE_LABEL = Label(GUI, textvariable=RED_SCORE, font=("times", 250, 'bold'), bg="red", justify=CENTER)
RED_SCORE_LABEL.pack()
RED_SCORE_LABEL.place(relx=0.75, rely=0.5, anchor='center')

#####################################################################################################

'''
Key Press Mapping:
    * RED SCORE
        -> +1 = a
        -> +3 = b
        -> -1 = c
        -> -3 = d
    * BLUE SCORE
        -> +1 = e
        -> +3 = f
        -> -1 = g
        -> -3 = h
    * Clear Score
        -> i
    * End Game (Exit)
        -> q
'''
def key_pressed(event):
    global BLUE_SCORE
    global RED_SCORE
    global num
    ############### RED SCORE ###############
    if event.char == 'a':    
        #RED_SCORE.set(max(min(MAX_SCORE, RED_SCORE.get() + 1), MIN_SCORE))
        RED_SCORE.set(num)
    elif event.char == 'b':    
        RED_SCORE.set(max(min(MAX_SCORE, RED_SCORE.get() + 3), MIN_SCORE))
    elif event.char == 'c':    
        RED_SCORE.set(max(0, RED_SCORE.get() - 1))
    elif event.char == 'd':    
        RED_SCORE.set(max(0, RED_SCORE.get() - 3))
    ############### BLUE SCORE ###############
    elif event.char == 'e':
        BLUE_SCORE.set(max(min(MAX_SCORE, BLUE_SCORE.get() + 1), MIN_SCORE))
    elif event.char == 'f':
        BLUE_SCORE.set(max(min(MAX_SCORE, BLUE_SCORE.get() + 3), MIN_SCORE))
    elif event.char == 'g':
        BLUE_SCORE.set(max(0, BLUE_SCORE.get() - 1))
    elif event.char == 'h':
        BLUE_SCORE.set(max(0, BLUE_SCORE.get() - 3))
    ############### CLEAR ###############
    elif event.char == 'i':
        BLUE_SCORE.set(0)
        RED_SCORE.set(0)
    ############### QUIT ###############
    elif event.char == 'q':
        exit()        

#####################################################################################################

# Event handler for key press
GUI.bind('<Key>', key_pressed)
# Startup in full screen mode
GUI.attributes('-fullscreen', True)

time.sleep(3)
ret, depth_back, color_back = dc.get_frame()
gray_back = cv2.cvtColor(color_back, cv2.COLOR_BGR2GRAY)[20:470, 140:460]
# Execute Image Processing Algorithm
def ImageProcessing():
    #ret, depth_back, color_back = dc.get_frame()
    
    
    ret, depth_frame, color_frame = dc.get_frame()
    cropped = color_frame[20:470, 140:460]
    depth = depth_frame[20:470, 140:460]  
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    gray = cv2.absdiff(gray, gray_back)


    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)[1]
    contoursArr = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contoursArr = imutils.grab_contours(contoursArr)
    num = len(contoursArr)
    print(num)
    RED_SCORE.set(num)
    #exit()

    
    
    
    GUI.after(100, ImageProcessing)

GUI.after(100, ImageProcessing)
GUI.mainloop()
