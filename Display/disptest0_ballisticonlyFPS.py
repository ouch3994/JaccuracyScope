import ST7789  
from PIL import Image  
from time import sleep 
import time
from PIL import ImageFont 
from PIL import ImageDraw
from PIL import ImageChops
import sys
import ballistics_test2 as ballistic
import numpy as np
import math

import io 
#import cv2


#image=Image.new('RGB',(240,240),(255,0,0))  #('RGB',(240,240),(r,g,b))
#display.display(image)  
#sleep(2)  
#mode directory here: /usr/local/lib/python3.7/dist-packages/ST7789  



sleep(0.5)





distance = 485.0
inc= 1
pos = 270




looper= True;

 
while (looper == True):
    fpsave =0 
    
    for i in range (1,30,1): #100
        t_start = time.time()
        
   
        
        
        
        #############################    BALLISTICS CALCULATION ################################
        distance = 800 # Lasered,  will update later yds
        distance_m = distance * 0.9144;
        
        
        #inputs 
        startheight  = 0 #meters 
        
        
        #From Sensor Thread, Always updating in backgorund 
       
        pitch = 0.001
    
        
        
        vstart= 2600*0.3048; #mps   #input 2600 from settings somewhere... with space.. 
        pitch_d = pitch * 57.2957795
        pitch_fake = (4/60) * math.pi /180
        
        
        Vx0x = round ( float(vstart * math.cos(pitch)) ,2 ) 
        Vy0y = round ( float(vstart * math.sin(pitch)) , 2 ) 
        
        pos = 0
        
        #solve 
        solution, plot = ballistic.solveBallistics(x0=0,y0=startheight,Vx0=795.0,Vy0=.05,dist_targ = distance,elevation0 = pitch) #takes lots of time . need paralell
        #solution = [1140,-300, 300, 499]
        #results
        
        hit = ((solution[1] - math.sin(pitch - pitch_fake)*distance))
        dropmoa = (-pitch + math.atan(solution[1]/solution[0]))*(180 / math.pi ) *60  #Needs looked at, scope height

        
        #END STATE CALCULATIONS   
        
        t_end = time.time()
        
        fps = -1/(t_start - t_end)
        fpsave = fpsave + fps
        
        

        
    
    fpsave = fpsave/30#00 
    print("Display: " + str("{:.2f}".format(fpsave)) )# _+ "  Camera:  " + str("{:.2f}".format(fpsCAM)) + "  Sensors:  " + str("{:.2f}".format(fpsSensor)))
    #print("Heading: " + str("{:.2f}".format(head)) + "  Pitch_:  " + str("{:.2f}".format(pitch_d)) + "  Roll:  " + str("{:.2f}".format(roll)))
    
    #print("Camera:  " + str("{:.2f}".format(fpsCAM)))    # "{:.2f}".format(
    #looper= False;
