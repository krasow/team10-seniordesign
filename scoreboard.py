# tkinter : python3 -m pip install tk
# pynput  : puthon3 -m pip install pynput

from pynput.keyboard import Key, Controller
from tkinter import *
import tkinter
from tkinter import messagebox

#####################################################################################################
#                           Setup GUI and display initial score                                     #
#####################################################################################################

# Initialize global variables for score
global scoreBLUE, scoreRED; scoreBLUE = scoreRED = 0
global MAX_SCORE, MIN_SCORE; MAX_SCORE = 21; MIN_SCORE = 0

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
BLUE_SCORE_LABEL = Label(GUI, textvariable=BLUE_SCORE, font=("times", 200, 'bold'), bg="blue", justify=CENTER)
BLUE_SCORE_LABEL.pack()
BLUE_SCORE_LABEL.place(relx=0.25, rely=0.5, anchor='center')

# Create the red player's score label
RED_SCORE = IntVar()
RED_SCORE.set(scoreRED)
RED_SCORE_LABEL = Label(GUI, textvariable=RED_SCORE, font=("times", 200, 'bold'), bg="red", justify=CENTER)
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
    ############### RED SCORE ###############
    if event.char == 'a':    
        RED_SCORE.set(max(min(MAX_SCORE, RED_SCORE.get() + 1), MIN_SCORE))
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

# Execute Image Processing Algorithm
def ImageProcessing():
    #ImageProcessing()
    GUI.after(500, ImageProcessing)

GUI.after(500, ImageProcessing)
GUI.mainloop()