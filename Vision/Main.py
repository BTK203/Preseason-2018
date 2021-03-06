###############################################
#    _____________________________________    #
#                                             #
#          VISION PROCESSING!!!!              #
#    Program to do some intense vision        #
#    processing by Brach Knutson.             #
#    _____________________________________    #
#                                             #
###############################################

#    __________________________________       
#    Algorithm:                               
#    1). Get image                          
#    2). Threshold image                      
#    3). Dilate image
#    4). convert to binary 
#    5). Find contours                        
#    6). run area test on contours    
#    7). run aspect ratio test on contours
#    8). get center point of remaining contour (if it exists)
#    9). Send values to other program to send 
#         to roboRIO (if #8 runs)
#   ____________________________________     
#    OTHER REMARKS:                           
#    --its being cleaned dont worry
#    ____________________________________

#dont move, needs to be at beginning
from __future__ import division
from __future__ import print_function

#import the other vision files
import Settings
import Thread1
import Thread2
import UI
import Utilities

#required packages
import numpy
import cv2
import threading
import time
import socket #for UDP
import Tkinter as tk
from decimal import *


def Watch():
    #Watches over all threads and outputs displays if told to.
    #threads in case one of them errors out
    print("Waiting for threads to initalize")
    time.sleep(1.5) #give the threads a little more time to start
    print("Starting...")
    while True:

        if Utilities.ProgramEnding: #but first lets check to see if the ending flag is up
                print("Vision man is going away now...")
                UI.Master_Window.destroy() # say goodbye to settings and output window
                break #stop loop is the program ending flag is up
    
        if Settings.DEVMODE:
            UI.UpdateUI() #updates the UI with updated values such as box center, contour data, etc
            UI.UpdateOutputImage() #updates the output image with the contour at the center
        else:
            #not devmode, we should print the coordinates out
            print("(" + str(Utilities.BoxCenterX) + ", " + str(Utilities.BoxCenterY) + ")", end='\r')
        
        Utilities.CheckThreadConditions()
        
        #send values to the RoboRIO.
        sendX = -1
        sendY = -1
        if (Utilities.BoxCenterX > -1) and (Utilities.BoxCenterY > -1):
            sendX = int( (Utilities.BoxCenterX / 200) * 1280 ) #scales to 720p resolution
            sendY = int( (Utilities.BoxCenterY / 200) * 720 )

        UDPMessage = str(sendX) + "," +str(sendY) #our message!
        Utilities.MainThreadMessage = "\nSending to the RIO: " + UDPMessage
        Utilities.sock.sendto(UDPMessage, (Settings.UDP_IP, Settings.UDP_PORT)) #haha this is what actually sends it
     
#starts the program and creates different threads and things for the things to run on.
def Vision():
    #start the stuff going
    if Utilities.Stream.isOpened():
        #initialize the threads
        if Settings.DEVMODE: #gives you the good stuff, but a bit harder on the CPU
            UI.InitUI()

        else:
            print("Initializing in Running Mode.\r\n\r\n") #runner mode is lighter on CPU but does not give you any feedback whatsoever (it just gives you the center box point)

        print("Hello. I am the vision man.")
        print("Making Threads")
        
        Utilities.THREAD_1 = Thread1.Thread1(1, "Thread 1", 1) # creates and starts new thread running Thread1(), to take and process the images
        Utilities.THREAD_2 = Thread2.Thread2(2, "Thread 2", 2) # creates and starts new thread running Thread2(), to process contours and come up with a center point

        print("Starting Threads")
        #start the threads
        Utilities.THREAD_1.start()
        Utilities.THREAD_2.start()

        print("Starting watch loop")
        Watch() #starts master loop
    else:
        print("WARNING: COULD NOT OPEN THE CAMERA")
        quit() #end program right then and there 

#main entry
if __name__ == '__main__': #MAIN ENTRY POINT RIGHT HERE
    try:
        Vision() #STARTS THE PROGARM!!
    except KeyboardInterrupt:
        Utilities.Kill() #displays set values and quits
