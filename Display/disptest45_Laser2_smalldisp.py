#Display? 
MinidisplayOption =  True

BigdisplayOption =  False #False  True 

if BigdisplayOption:
    from tkinter import *
    
import ST7789  
from PIL import Image 

if BigdisplayOption:
    from PIL import ImageTk as dingerr
    
from time import sleep 
import time
from PIL import ImageFont 
from PIL import ImageDraw
from PIL import ImageChops
import sys
#import ballistics_test2 as ballistic
import numpy as np
import math

import io 

import CamThreaderSLOWFPS as CamThreader

import SensorThreaderSlowerRotaryEncodersTRY as SensorThreader 

import BallisticThreader4PrinterAndLaserL   as BallisticThreader

import RPi.GPIO as GPIO 

from gpiozero import CPUTemperature

from numpy import load
from numpy import save


#########MEasure Temp       vcgencmd measure_temp


#Video Flag 
import cv2

#Record Video 
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

recordVideo = False 



GPIO.setmode(GPIO.BCM)

##Big Display 
###J_UP = 6
###J_DOWN = 19
###J_LEFT = 5
###J_RIGHT = 26
###J_CENTER = 13
###J_1 = 21
###J_2 = 20
###J_3 = 16
###GPIO.setup(J_UP, GPIO.IN,pull_up_down=GPIO.PUD_UP) ######buttons so you dont short shit lol 
###GPIO.setup(J_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_LEFT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_RIGHT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_CENTER,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
###GPIO.setup(J_3, GPIO.IN,pull_up_down=GPIO.PUD_UP) 



###Little Display 
J_1 = 24
J_2 = 23
J_3 = 27

#J_UP = 6
#J_DOWN = 19
#J_LEFT = 5
#J_RIGHT = 26
#J_CENTER = 13
##J_1 = 21
##J_2 = 20
#J_alt = 16


GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_3, GPIO.IN,pull_up_down=GPIO.PUD_UP) 

#GPIO.setup(J_UP, GPIO.IN,pull_up_down=GPIO.PUD_UP) ######buttons so you dont short shit lol 
#GPIO.setup(J_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_LEFT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_RIGHT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_CENTER,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_alt, GPIO.IN,pull_up_down=GPIO.PUD_UP)


cpu = CPUTemperature()
 
 
if BigdisplayOption:
    # Create an instance of TKinter Window or frame
    win = Tk()
    win.bind('<Escape>', lambda e: app.quit())
    
    # Set the size of the window
    #win.geometry("240x240")
    win.geometry("480x480")
    
    # Create a Label to capture the Video frames
    label =Label(win)
    label.grid(row=0, column=0)
    label.configure(bg='black')



 
#st77789  backlight=24,rotation=180, rst = 27,
disp=ST7789.ST7789(height=240, width=240, port=0, cs=0,dc=25,rotation=0,spi_speed_hz=62500*1000)   #dc5 160000000 48000000
disp._spi.mode=3  
disp.reset()  
disp._init()  
#image=Image.new('RGB',(240,240),(255,0,0))  #('RGB',(240,240),(r,g,b))
#display.display(image)  
#sleep(2)  
#mode directory here: /usr/local/lib/python3.9/dist-packages/ST7789  



MESSAGE = "Wind: 5.0 mph"
wind = 0;

WIDTH = 240 #disp.width
HEIGHT = 240 #disp.height
##disp.set_window(x0=0, y0=0, x1=239, y1=239)
img=Image.open("/home/pi/share/Display/LoadingScreen2.jpg")  
img=img.resize((240,240),resample=Image.LANCZOS) 
disp.display(img,xs=0,xe=239,ys=0,ye=239)


if BigdisplayOption:
    # Convert image to PhotoImage
    img2x=img.resize((480,480),resample=Image.NEAREST) 
    imgtk = dingerr.PhotoImage(image = img2x)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.update()  

sleep(5)


### AFter sleep, load the last configs and set them to the Ballistic Threader :) 
Loaddata = load("/home/pi/share/Display/configData.npy")
BallisticThreader.thread.caliber = Loaddata[0,0]
BallisticThreader.thread.bullet_weight_grain = int(Loaddata[0,1])
BallisticThreader.thread.Gsolver = int(Loaddata[0,2])
BallisticThreader.thread.bc7_box = Loaddata[0,3]
BallisticThreader.thread.zerodistance = Loaddata[0,4]
BallisticThreader.thread.fps_box = int(Loaddata[0,5])
BallisticThreader.thread.windspeed = Loaddata[0,6]
BallisticThreader.thread.wind_head_deg = Loaddata[0,7]
BallisticThreader.thread.Atm_altitude = Loaddata[0,8]
BallisticThreader.thread.Atm_pressure = Loaddata[0,9]
BallisticThreader.thread.Atm_temperature = Loaddata[0,10]
BallisticThreader.thread.Atm_RelHumidity  = Loaddata[0,11] 
focallength = Loaddata[0,12]

BallisticThreader.thread.ResolveAngle = True





#disp.set_window(x0=0, y0=0, x1=10, y1=10)
blackframe = Image.new('RGB', (240, 240), color=(0, 0, 0))
img = Image.new('RGB', (240, 240), color=(0, 0, 0))
disp.display(img,xs=0,xe=239,ys=0,ye=239) #gotta match draw dimensions 
draw = ImageDraw.Draw(img)
#disp.display(img,xs=0,xe=0,ys=239,ye=239)


if BigdisplayOption:
    # Convert image to PhotoImage
    img2x=img.resize((480,480),resample=Image.NEAREST) 
    imgtk = dingerr.PhotoImage(image = img2x)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.update() 



image2=Image.open("/home/pi/share/Display/COMPASS4.jpg")   
image2=image2.resize((180,7),resample=Image.LANCZOS)


image_lob=Image.open("/home/pi/share/Display/lobstermodebase2.jpg")   

image_settings=Image.open("/home/pi/share/Display/SettingsMenuBase5.jpg")   #was 4 
image_settingsP2 = Image.open("/home/pi/share/Display/SettingsMenuBasePAGE2.jpg")

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)

font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)

fontL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

SettingsFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)


size_x, size_y = draw.textsize(MESSAGE, font)

text_x = disp.width
text_y = (disp.height -size_y) //2        #(disp.height - size_y) // 2

t_start = time.time()
fps = 0 



imgcount = 1 ; 


distance = 500
inc= 1
pos = 270

fpsCAM  = CamThreader.thread.fpsaveout
fpsavefr= 0 
   


looper= True;

ChooseSolver = "GNUsolver"  #"Jacksolver"   or "GNUsolver" 
BallisticThreader.thread.solver = ChooseSolver
#BallisticThreader.thread.solver = "GNUsolver"


#variables needed for impact Preview box and smoothing 
flash = True; 
droppixelsAverage = 0 
windpixelsAverage = 0 
filtersize = 24
droppixelpool = np.zeros(filtersize)
windpixelpool = np.zeros(filtersize)

dropcounter = 0 


#starting Zoom of camera 
CamThreader.thread.zoom = 1.0 # 1.0
zoomtest = False  #was false
zoomtester = 0
zoomincrease = 1 

sleep(1)



#Mode Tester! 
Scope_mode = 0 #0 main   1 Lobster    2 Settings  3 FF mode   4  Atm settings 
modecounter = 0 
modecycletest = False

#Crosshairs 
drawsubhashes = True

#Drawsubsubs 
drawsubsubs  = True


#menu fo the settings 
menuNumber= 0;
settingAdjustNumber = 0.000; 

#needed hard 
#focallength = 77.25 #mm ########OHHHH THIS IS SHITTY    #.75 facto roff... try 77.25 not 103
#Focal Length is now set by the config file :))) adjust with Scope Mode 3 

#opticres = 14.0752366 #pixels per MOA 
opticres = 1 / ((math.atan(0.00155 / focallength)*57.295779513)*60)
print("opticalResolution is ")
print(opticres)
print("Pix per MOA ")

opticPercent = opticres/3040


#scopeOFFsets 
scopexoffset = 0   #angle right 20  MOA 
scopeyoffset = 0 #angle up 40 MOA 
inputXShift = 0 
inputYShift = 0 

takeimage = 0 

changeOpitcs = 0


encoder2Mode = "Zoom" ; # "Wind" or "Zoom" 

debounce1 = False; 
debouncer1 = 0 
debounce2 = False;
debouncer2 = 0;



CamThreader.thread.clicky   = int(scopeyoffset  * opticres)
CamThreader.thread.clicky   = int(scopeyoffset  * opticres) 


printNow = False; 

LaserOn = False; 




def show_frames(imger):
   # Get the latest frame and convert into Image


   # Convert image to PhotoImage
   imger2x=imger.resize((480,480),resample=Image.NEAREST) 
   imgtk = dingerr.PhotoImage(image = imger2x)
   #label.imgtk = imgtk
   label['image']=imgtk
   # Repeat after an interval to capture continiously
   label.update()

   











def main(): 
    global Scope_mode, video, zoomtester, dropcounter,distance,debouncer1, debounce1,debouncer2, debounce2,encoder2Mode, drawsubhashes, drawsubsubs, fpsavefr, settingAdjustNumber, menuNumber,inputXShift, inputYShift, scopeyoffset,scopexoffset, flash, zoomincrease, menuNumber, takeimage,focallength,opticPercent,opticres, changeOpitcs
    #global zoomtester
    #global dropcounter
    #global fpsavefr
    #global flash
    #global zoomincrease
       
    while (looper == True):
        fpsave =0 
        
        for i in range (1,30,1): #100 #FPS CALCUALTOR 
            t_start = time.time()
    
            
            
    
            
            ############################   TROUBLE SHOOT  MODES  SWITCHER      #######################
            if (modecycletest):
                #mode selector :) 
                modecounter += 1 
    
                if (modecounter == 200 ):   #every 100 frames, change the unit mode.  
                    modecounter = 0 #reset counter 
                    
                    if (Scope_mode == 2):
                        Scope_mode = 1 
                    else: 
                        Scope_mode = 2
            ############################   TROUBLE SHOOT  MODES  SWITCHER      #######################        
            
            
            
            
            #From Sensor Thread, Always updating in backgorund 
            head = SensorThreader.thread.output_heading
            pitch = -SensorThreader.thread.pitch - (4.3 / 57.2957795)
            roll = SensorThreader.thread.roll
            fpsSensor  = SensorThreader.thread.fpsaveout
            pitch_d = pitch * 57.2957795;
            
            if (changeOpitcs ==1 ):
                opticres = 1 / ((math.atan(0.00155 / focallength)*57.295779513)*60)
                opticPercent = opticres/3040  #was 3040 or 4056v 
                changeOpitcs = 0
            
            
            if ( Scope_mode == 0):   #0 is regular scope #1 is LOBSTER mode 
                BallisticThreader.thread.ScopeMode =0;
                BallisticThreader.thread.dt = 0.05
                BallisticThreader.thread.T = 3
            
            
            
                pasteimage4 = CamThreader.thread.imageout # get new frame from thread 
                fpsCAM  = CamThreader.thread.fpsaveout  #grab the output 
                #pasteimage4.show() #FOR DEBUG ONLY DONT USE LOOPING OPENS WINDOW 
                pasteimage4=pasteimage4.resize((240,180),resample=Image.NEAREST) #BIG FPS nearest is fast 
                
                
                ##################### Rotary Encoder INPUTS    ################################################
                
                
                #Encoder 1 Algorithm (Adjustments when zoomed)
                if (CamThreader.thread.zoom < (1/2.0)):
                    #adjust the Elevation
                    if (SensorThreader.thread.encoder1Output !=  0 ):
                        inputYShift = inputYShift + (SensorThreader.thread.encoder1Output)
                        SensorThreader.thread.encoder1Output = 0
                    #adjust Wind 
                    if(encoder2Mode == "Wind"): 
                        if (SensorThreader.thread.encoder2Output !=  0 ):
                            inputXShift = inputXShift + (SensorThreader.thread.encoder2Output)
                            SensorThreader.thread.encoder2Output = 0      
                        
                    
                    if (SensorThreader.thread.enc1_button_held == True and debounce1 == False):
                        print("Snapping Outward! ")
                        CamThreader.thread.zoom = 1.0
                        inputXShift = 0
                        inputYShift = 0 
                        debounce1 = True;
                        
                        
                elif (CamThreader.thread.zoom == 1.0 and debounce1 == False):
                    if (SensorThreader.thread.encoder1Output !=  0 ):
                        newdist = distance + (SensorThreader.thread.encoder1Output * 25)
                        if(newdist < 25):
                            distance=25;
                            SensorThreader.thread.encoder1Output = 0
                        else: 
                            distance = newdist
                            SensorThreader.thread.encoder1Output = 0                
                    if (SensorThreader.thread.enc1_button_held == True):
                        print("Snapping Inward! ")
                        CamThreader.thread.zoom = 0.125
                        inputXShift = int(-windmoa)
                        inputYShift = int(-dropmoa)
                        debounce1 = True; 
                        
                if (encoder2Mode == "Zoom"): 
                    #zoom the camera in on encoder 2 inputs...
                    if (SensorThreader.thread.encoder2Output !=  0 ):
                        newzoom = CamThreader.thread.zoom/(pow(1.1,SensorThreader.thread.encoder2Output)) 
                        print ("new zoom is: " + str(newzoom))
                        if (newzoom > 1.0):
                            CamThreader.thread.zoom = 1.0
                        elif (newzoom < 0.0625):
                            CamThreader.thread.zoom = 0.0625
                        else: 
                            CamThreader.thread.zoom = newzoom
                        SensorThreader.thread.encoder2Output = 0    
                            
                        
                        
                if (SensorThreader.thread.enc2_button_held == True and debounce2 == False):
                    if(encoder2Mode == "Wind"): 
                        encoder2Mode = "Zoom";
                        print("Changed ENC2 to Zoom Mode")
                    else: 
                        encoder2Mode = "Wind";
                        print("Changed ENC2 to Wind Mode")                                              
                    debounce2 = True;                         


                #Debounce Encoder Pressed 
                if(debounce1 == True): 
                    debouncer1 += 1
                    #print("debouncing....")
                    if (debouncer1  > 10): 
                        debounce1 = False;
                        debouncer1 = 0;
                        
                if(debounce2 == True): 
                    debouncer2 += 1
                    #print("debouncing....")
                    if (debouncer2  > 10): 
                        debounce2 = False;
                        debouncer2 = 0;                        
                
                
                
                #correct the bullshit math i cant figure out.... 
                if (CamThreader.thread.zoom > (1/2.0)): #2.9
                    scopexoffset = 0   #angle right 20  MOA 
                    scopeyoffset = 0 #angle up 40 MOA 
                    CamThreader.thread.clickx   = int(scopexoffset  * opticPercent* 3040)     #for Mode 1 camera 1080 or 2028  3040for mode 2
                    CamThreader.thread.clicky   = int(scopeyoffset  * opticPercent* 3040)               
                else: 
                    scopexoffset = inputXShift  #angle right 20  MOA 
                    scopeyoffset = inputYShift                  #angle up 40 MOA 
                    CamThreader.thread.clickx   = int(scopexoffset  * opticPercent* 3040)
                    CamThreader.thread.clicky   = int(scopeyoffset  * opticPercent * 3040)
                    #print(CamThreader.thread.clicky)
                    
                    
                    
                #If detected new laser results are in .... 
                
                if(BallisticThreader.thread.newLaserDistance == True):
                    tdistance = BallisticThreader.thread.distancelaser; 
                    if (tdistance > 5 ):
                        distance = tdistance
                        BallisticThreader.thread.newLaserDistance = False; 
                
                
                
                
                ######################CAMERA ZOOM TEST,  cranks between 1.0 down to 0.0625.  
                if (zoomtest):
                    zoomtester += 1 
                    
                    
                    if (zoomtester == 2): #every 12 frames zoom/unzoom  75  
                        zoomtester = 0
                        
                        if (zoomincrease == 1):
                            CamThreader.thread.zoom = CamThreader.thread.zoom/1.01  #/2
                            #scopexoffset = (scopexoffset + .125) 
                        # scopeyoffset = (scopeyoffset + (.1)) 
                            #CamThreader.thread.clickx   = int(scopexoffset  * 14)
                            #CamThreader.thread.clicky   = int(scopeyoffset  * 14)
                            
                            if (CamThreader.thread.zoom < (0.0626)):   
                                zoomincrease = 0 
                                        
                        else: 
                            CamThreader.thread.zoom = CamThreader.thread.zoom*1.01 #*2
                            #scopexoffset = (scopexoffset -.125) 
                            #scopeyoffset = (scopeyoffset - (.1) ) 
                            #CamThreader.thread.clickx   = int(scopexoffset * 14)
                            #CamThreader.thread.clicky   = int(scopeyoffset  * 14)
                            if (CamThreader.thread.zoom > (0.90)):
                                zoomincrease = 1             
                        
                    
                
                
                
                
                #############################    BALLISTICS CALCULATION ################################
                #distance = 125 # Lasered,  will update later yds
                distance_m = distance * 0.9144;

                    
                
            
                
                #inputs 
                startheight  = 0 #meters 
                
                
                #From Sensor Thread, Always updating in backgorund 
                #head = SensorThreader.thread.output_heading
                #pitch = -SensorThreader.thread.pitch #- 0.01308997
                #roll = SensorThreader.thread.roll
                #fpsSensor  = SensorThreader.thread.fpsaveout
                
                wobbleY = SensorThreader.thread.wobbleY
                wobbleX = SensorThreader.thread.wobbleX
                wobble_radius = (math.sqrt((wobbleY*wobbleY)+(wobbleX*wobbleX))) + 2  
                sight_angle = ( BallisticThreader.thread.gunSightangle * math.pi/180)#rads 
                
                
                vstart= 2600*0.3048; #mps   #input 2600 from settings somewhere... with space.. 
                #pitch_d = pitch * 57.2957795
                pitch_fake = (4/60) * math.pi /180
                    
                Vx0x = round ( float(vstart * math.cos(pitch-sight_angle)) ,2 ) 
                Vy0y = round ( float(vstart * math.sin(pitch-sight_angle)) , 2 ) 
                
                
                
                pos = head
                
                #Standard input vals to the ballthreader 
                BallisticThreader.thread.x0in = 0.0
                BallisticThreader.thread.y0in = startheight
                BallisticThreader.thread.Vx0in = Vx0x
                BallisticThreader.thread.Vy0in = Vy0y
                BallisticThreader.thread.targetdistin =  distance_m
                
                if (BallisticThreader.thread.solver == "GNUsolver"):
                    BallisticThreader.thread.elevation0in = pitch_d
                else: 
                    BallisticThreader.thread.elevation0in = pitch
                
                
                        #Wind Inputs for Solution 
                BallisticThreader.thread.facing = head  

                
                
                fpsBalls = BallisticThreader.thread.fpsaveout
                
                solution = BallisticThreader.thread.solution
                plot = BallisticThreader.thread.plotter
                
                timeOfFlight =  solution[5]
            
                
                
                
                #solution, plot = ballistic.solveBallistics(x0=0,y0=startheight,Vx0=795.0,Vy0=.05,dist_targ = distance_m,elevation0 = pitch) #takes lots of time . need paralell
                #solution = [1140,-300, 300, 499]
                
                #REsults
                hit = ((solution[1] - math.sin(pitch - pitch_fake)*distance))
                
                if (BallisticThreader.thread.solver == "GNUsolver"):
                    dropmoa = solution[6]
                    #dropmoa = -40
                else: 
                
                    #print(solution)
                    dropmoa = (-pitch + math.atan((solution[1]-((BallisticThreader.thread.scope_height*0.0254)+startheight))/solution[0]))*(180 / math.pi ) *60 - (BallisticThreader.thread.gunSightangle*60) #Needs looked at, scope height
                    #dropmoa   = ((solution[1] - startheight-(BallisticThreader.thread.scope_height*0.0254))*39.3701) / ((solution[0]/91.44) * 1.047) #works????????? idk lol 
                    #dropmoa = ((solution[1]-startheight)*39) * 91.44 / (solution[0] * 1.047) - (BallisticThreader.thread.gunSightangle*60)
                    
                ##print(dropmoa);
                if (BallisticThreader.thread.solver == "GNUsolver"):
                    windmoa = solution[4]
                    #windmoa = -20
                else: 
                    windmoa = -(math.atan(solution[4]/solution[0]))*(180 / math.pi ) * 60
                
                #print(windmoa)
                
                
                #Convert the drop MOA to pixels relative to dead center :)          
                
                
    #           dropmoa_pix = ((dropmoa)*opticres)  #drop in net rull res pixels  Opposite for the dispaly
    #           windmoa_pix =  (windmoa) * opticres 
                dropmoa_pix = ((dropmoa + scopeyoffset)*opticres)  #drop in net rull res pixels  Opposite for the dispaly
                windmoa_pix =  (windmoa + scopexoffset) * opticres 
                
                
                
                
    
                
                #Apply scaling of camera to droppixels 
                scaling = CamThreader.thread.zoom
                
            
                
                droppixelpool[dropcounter] = - (dropmoa_pix ) * 180 /scaling;
                windpixelpool[dropcounter] = - (windmoa_pix ) * 180 /scaling;
                dropcounter += 1 
                if (dropcounter > filtersize-1 ):
                    dropcounter = 0
                
                
                
                
                
                #apply mapping of resize to 240x240 screen to get impactzoneY
                #impactzoneX = np.average(windpixelpool) #no wind for now 
                #impactzoneY = np.average(droppixelpool) 
                #impactzoneX=- ( windmoa_pix / scaling )  / added_scale;
                
    
                impactzoneY= - ( (dropmoa + scopeyoffset) * opticPercent ) * 180 /scaling; #180image tall
                impactzoneX = - ( (windmoa + scopexoffset) * opticPercent ) * 180 /scaling; #hmmm its 240 wide tho... 
                
    
                
                
                
                
                
                ####################################PIL IMAGE GENERATION#######################################
                
                #Blank slate program. The ulimate tool for a master criminal trying to get a clean record 
                img.paste(blackframe,(0,0))
                
                
                ### Draw Camaera IMAGE
                img.paste(pasteimage4,(0,30))
                
                
                
                ##############WIND DISPLAYING  
                ### Draw CrossHair
                
                #draw.rectangle((119, 117, 119, 121), (255, 0, 0))
                #draw.rectangle((117, 119, 121, 119), (255, 0, 0))  
                
                
                oneMoaScreen = opticres
                
            
                
                subhashcolor= (0,255,0)
                markercolor = (255,255,255)
                subsubcolor = (255,0,0)
            
                markeroffsetX = -scopexoffset
                markeroffsetY = -scopeyoffset
                
                
                
                #Horizontal Line and hashes 
                draw.rectangle((0, 119, 239, 119), (255, 0, 0))  
                
                #Veritical 
                #straight red line  :)  
                draw.rectangle((119, 30, 119, 209), (255, 0, 0))
                    
                drawsubhasesroutine(draw, scaling, subhashcolor, drawsubsubs, subsubcolor,markeroffsetX,markercolor, markeroffsetY) #############################################################
######################################                                
                
                windbox_h = 21
                windbox_w = 78
                Yoffset = 8
                #replaced Wind with CPUtemp... put back to wind later...(mph)
                MESSAGE = "Wind: " + str("{:2.1f}".format(BallisticThreader.thread.windspeed)) + " mph"  + "\n Dir: " + str("{:.1f}".format(BallisticThreader.thread.wind_head_deg))  + " deg"
                
                draw.rectangle((239-windbox_w, Yoffset, 239, Yoffset+windbox_h), (0, 0, 0))  #disp.width, disp.heigh
                draw.text((239-windbox_w+10,Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255))
                
                
                #######DrawZoomLevel
                
                #thezoom = int(1/CamThreader.thread.zoom)
                MESSAGE = str("{:.1f}".format(1/CamThreader.thread.zoom)) + "x" 
                draw.text((2,180), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                
                
                #######Draw CPU Temps 
                MESSAGE = "CPU Temp: " + str("{:.1f}".format(cpu.temperature)) 
                
                tempy= cpu.temperature
                if(tempy < 55):
                    draw.text((2,195), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))   
                elif (tempy >= 55 and tempy < 80): 
                    draw.text((2,195), MESSAGE, spacing = 1, font=fontL, fill=(255, 180, 0)) 
                else:                   #TOO HOT WARNING 
                    draw.text((2,195), MESSAGE, spacing = 1, font=fontL, fill=(255, 0, 0)) 
                   

                   
                ##########Draw Time of Flight 
                MESSAGE = "ToF: " + str("{:.3f}".format(timeOfFlight) + "(s)") 
                draw.text((2,32), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                
                
                #######Draw Encoder 2 Mode
                MESSAGE = str(encoder2Mode) 
                draw.text((210,180), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                
                
                
                #######Draw Frame Rate
                MESSAGE = "FPS: " + str("{:2.1f}".format(fpsavefr)) 
                draw.text((190,195), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))                
                
  
                #######DrawScope Offsets 
                
                if (scopeyoffset!=0):
                    if (scopeyoffset>0):
                        MESSAGE ="Yoff: " + str("{:.2f}".format(-scopeyoffset)) 
                        draw.text((150,30), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))   
                    else: 
                        MESSAGE = "Yoff: " + "+" + str("{:.2f}".format(-scopeyoffset)) 
                        draw.text((150,30), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255)) 
    
                if (scopexoffset!=0):
                    if (scopexoffset>0):
                        MESSAGE = "L/R: "  + str("{:.2f}".format(-scopexoffset)) 
                        draw.text((175,100), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))   
                    else: 
                        MESSAGE = "L/R: " + "+"+ str("{:.2f}".format(-scopexoffset)) 
                        draw.text((175,100), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))                     
                
                
                ############# Draw Target DISTANCE DISPLAY 
                dirbox_h = 21
                dirbox_w = 78
                Yoffset = 8
                
                MESSAGE = "Dist: " + str("{:.2f}".format(distance)) + " yds"  + "\nElev: " + str("{:.2f}".format(pitch_d)) + " deg"
                
                draw.rectangle((0, Yoffset, dirbox_w, Yoffset+dirbox_h), (0, 0, 0))  #disp.width, disp.height
                draw.text((5, Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                
                
                
                
                ############# Draw MOA Solved DISPLAY 
                windbox_h = 31
                windbox_w = 63
                Yoffset = HEIGHT  - windbox_h - 3
                
                MESSAGE = "MOA SOLVED:" + "\nWind: " + str("{:.2f}".format(windmoa)) + "\nElev: " + str("{:.2f}".format(dropmoa)) 
                #MOA 
                draw.rectangle((WIDTH - windbox_w, Yoffset, WIDTH, Yoffset+windbox_h), (0, 0, 0))  #disp.width, disp.height
                draw.text((WIDTH - windbox_w, Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255))
                
                
                ############# Draw Compass  DISPLAY 
                image3=ImageChops.offset(image2,int(-pos/2-180),0)    
                img.paste(image3,(30,0)) #paste on existing image
                
                
                
                
                
                ############# Draw Compass Heading DISPLAY 
                compbox_h = 21
                compbox_w = 33
                Yoffset = 7
                
                
                
                MESSAGE = "   V " + "\n" +str("{:.2f}".format(pos))   ######TODO  was pos .2   SensorThreader.thread.lead*57.2958
                
                draw.rectangle((107,Yoffset,107+compbox_h+20 ,compbox_w + Yoffset-11), (0, 0, 0))  #disp.width, disp.height
                draw.text((107,Yoffset), MESSAGE, font=fontL, spacing = 1, fill=(255, 255, 255)) #int(text_x), int(text_y)  
                
                
                
                
###################################################################################
                
                ### Draw impact zone! (one by three area), flash it 
                
                
                
                if flash: 
                    flashcolor = (0,255,0) #red 
                    flash = not flash
                else: 
                    flashcolor = (120,255,0) #green
                    flash = not flash
            
                #Impact Cross 
                draw.line([((119 + impactzoneX - 3 ) ,  (119 + impactzoneY + 3 )   ), ( (119 + impactzoneX  + 3 )  , (119 + impactzoneY - 3 )  ) ], flashcolor, width = 1  )
                draw.line([((119 + impactzoneX + 3 ) ,  (119 + impactzoneY + 3 )   ), ( (119 + impactzoneX  - 3 )  , (119 + impactzoneY - 3 )  ) ], flashcolor, width = 1  )
            
                #impact Box 
                draw.line([((119 + impactzoneX - 3 ) ,  (119 + impactzoneY - 3 )   ), ( (119 + impactzoneX  - 3 )  , (119 + impactzoneY + 3 )  ) ], flashcolor, width = 1  )
                draw.line([((119 + impactzoneX + 3 ) ,  (119 + impactzoneY - 3 )   ), ( (119 + impactzoneX  + 3 )  , (119 + impactzoneY + 3 )  ) ], flashcolor, width = 1  )
                draw.line([((119 + impactzoneX - 3 ) ,  (119 + impactzoneY - 3 )   ), ( (119 + impactzoneX  + 3 )  , (119 + impactzoneY - 3 )  ) ], flashcolor, width = 1  )
                draw.line([((119 + impactzoneX - 3 ) ,  (119 + impactzoneY + 3 )   ), ( (119 + impactzoneX  + 3 )  , (119 + impactzoneY + 3 )  ) ], flashcolor, width = 1  )
            
                
                if (BallisticThreader.thread.printerGO == True):
                    draw.rectangle((69, 69, 169, 169), (0, 0, 255))
                    MESSAGE = " PRINTING .... "
                    draw.text((92,int(110+(pitch_d*1.5))), MESSAGE, font=fontL, spacing = 1, fill=(255, 255, 255)) #int(text_x), int(text_y)  
                
                
                
                ###Draw Stability Marker 
                
                indicatorcolor = (0,0,255) #blue 
                
                #print(indicatorcolor)
                centerx = 119 + impactzoneX
                centery = 119 + impactzoneY
                r = (wobble_radius*wobble_radius)/10
                shape = [((centerx-wobble_radius),(centery-wobble_radius)),((centerx+wobble_radius) , (centery+wobble_radius))]
                draw.arc(shape, start =0 , end = 360 , fill = indicatorcolor)
            
                
                
                ##########Draw the gyro offset!!!!!! yay lol 
                scanSpeed = SensorThreader.thread.lead*57.2958
                
                if (abs(scanSpeed) > 0.083):
                    leadAngle = timeOfFlight * scanSpeed * 60 #Deg/s times seconds *60 = angle (min of degrees)
                    
                    #convert  Lead Angle to Pixel swath by mulitply by.... 
                    leadradius =  leadAngle * opticPercent * 180 /scaling;  
                
                    #centerx = 119 + impactzoneX
                    #centery = 119 + impactzoneY  #centerd on the impact box... 
                    
                    #draw horizontal line, the width of the amount...  #######fix line 779 
                    
                    #if(scanSpeed < 0):
                    #
                    #    draw.line([((119 + impactzoneX ),  (119 + impactzoneY)   ), ( (119 + impactzoneX - leadradius ) , (119 + impactzoneY )  ) ], (255,255,255), width = 1  )
                    #    #Verticals on the ends 
                    #    draw.line([((119 + impactzoneX - leadradius ),  (119 + impactzoneY-4)   ), ( (119 + impactzoneX - leadradius ) , (119 + impactzoneY +4)  ) ], (255,150,10), width = 1  )
                    #
                    #else: 
                    draw.line([((119 + impactzoneX ),  (119 + impactzoneY)   ), ( (119 + impactzoneX + leadradius ) , (119 + impactzoneY )  ) ], (255,150,10), width = 1  )
                    draw.line([((119 + impactzoneX + leadradius ),  (119 + impactzoneY-4)   ), ( (119 + impactzoneX + leadradius ) , (119 + impactzoneY +4)  ) ], (255,150,10), width = 1  )
                    
                    
                    #debug
                    #print(str(scanSpeed*60)  + "modps?    " +  str(leadAngle) + " degrees lead")
                   
                
                
                
                ####Draw the Plot at bottom using Paste Function 
                img.paste(plot,(0,240-30))  

                ###Draw the Record thing 
                if (recordVideo == True):
                
                    draw.ellipse((214,32,219,37),fill=(255, 0, 0), outline =(255, 0, 0))    
                    MESSAGE = "REC" 
                    draw.text((221,32), MESSAGE, spacing = 1, font=font, fill=(255, 0, 0)) 
                    
   
                
                ### draw LASERING 
                
                if (BallisticThreader.thread.Lasering == True): 
                    MESSAGE = "LASERING..." 
                    draw.text((150,42), MESSAGE, spacing = 1, font=fontL, fill=(255, 10, 10))
                    
    
                
                
                
                
                
                # Convert image to PhotoImage
                
                if BigdisplayOption:
                    show_frames(img)
                
                ######## Send created image to the Display on SPI fast  
                #disp.display(img,xs=0,xe=239,ys=0,ye=239) #,xs=0,xe=239,ys=0,ye=239)  
                if MinidisplayOption: 
                    disp.displayFast(img)
                    
                
                if (takeimage ==1):                
                    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
                    img.save(name, format="png") 
                    takeimage = 0 
                    
                    
                #MOVE TO ALL OTHER INSTANCES 
                if (recordVideo == True):  
                    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
                    
                     
    
                
            
            
            elif (Scope_mode == 1):   #LOBSTER MODE 
                BallisticThreader.thread.ScopeMode =1;    #Scope_mode
                BallisticThreader.thread.dt = 2
                BallisticThreader.thread.T = 60
                
                img.paste(image_lob,(0,0))
                
                #draw.rectangle((0,0,239,239), (0, 0, 0))  #disp.width, disp.height  #not needed. keep for reference later? 
                
                #img.paste(blackframe,(0,0))  
    
                #############################    BALLISTICS CALCULATION ################################
                #distance = 125 # Lasered,  will update later yds
                distance_m = distance * 0.9144;
                
                target_elevation =  math.radians(10) # degrees to rads  ########### TODO NOT IMPLEMENTED YET 
                
            
                
                #inputs 
                startheight  = 0 #meters 
                
                
                #From Sensor Thread, Always updating in backgorund 
                #head = SensorThreader.thread.output_heading
                #pitch = -SensorThreader.thread.pitch
                #roll = SensorThreader.thread.roll
                #fpsSensor  = SensorThreader.thread.fpsaveout
                
                wobbleY = SensorThreader.thread.wobbleY
                wobbleX = SensorThreader.thread.wobbleX
                wobble_radius = (math.sqrt((wobbleY*wobbleY)+(wobbleX*wobbleX))) + 2  
                sight_angle = (BallisticThreader.thread.gunSightangle * math.pi/180)#rads 
                
                
                vstart= 2600*0.3048; #mps   #input 2600 from settings somewhere... with space.. 
                #pitch_d = pitch * 57.2957795
                pitch_fake = (4/60) * math.pi /180
                    
                Vx0x = round ( float(vstart * math.cos(pitch+sight_angle)) ,2 )  ########Check sight angle method... fuck 
                Vy0y = round ( float(vstart * math.sin(pitch+sight_angle)) , 2 ) 
                            
                pos = head
                
                #Standard input vals to the ballthreader 
                BallisticThreader.thread.x0in = 0.0
                BallisticThreader.thread.y0in = startheight
                BallisticThreader.thread.Vx0in = Vx0x
                BallisticThreader.thread.Vy0in = Vy0y
                BallisticThreader.thread.targetdistin =  2500 * 0.9144
                BallisticThreader.thread.elevation0in = pitch
                
                        #Wind Inputs for Solution 
                BallisticThreader.thread.facing = head  
                BallisticThreader.thread.windspeed = 0
                BallisticThreader.thread.wind_head_deg = 0
                
                
                fpsBalls = BallisticThreader.thread.fpsaveout
                
                solutionLob = BallisticThreader.thread.solution
                plotLob = BallisticThreader.thread.plotter            
                
                
                ####Draw the Plot at bottom using Paste Function 
                img.paste(plotLob,(0,0))  
                
                
                ##Draw Score 
                
                howhighdiditgo = BallisticThreader.thread.maxheight*3.28084/1000
                #print(howhighdiditgo)
                
                
                MESSAGE = str(int(solutionLob[0]*1.09361)) + " yds far!!" 
                draw.text((50, 150), MESSAGE, spacing = 1, font=font2, fill=(255, 255, 255))
                MESSAGE = str("{:.2f}".format(howhighdiditgo)) + " kft high!" 
                draw.text((50, 170), MESSAGE, spacing = 1, font=font2, fill=(255, 255, 255))
                
                #Draw the Stats at bottom 
                        
                ############# Draw Target DISTANCE DISPLAY 
                dirboxlo_h = 29
                dirboxlo_w = 63
                Yoffset = HEIGHT  - dirboxlo_h - 3+3
    
                MESSAGE = "Dist: " + str("{:.2f}".format(solutionLob[0]*1.09361)) + " yds"  + "\nElev: " + str("{:.2f}".format(pitch_d)) + " deg"
                
                draw.rectangle((0, Yoffset, dirboxlo_w, Yoffset+dirboxlo_h), (0, 0, 0))  #disp.width, disp.height
                draw.text((5, Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                
                
                
                #Display on GUI 
                if BigdisplayOption:
                    show_frames(img)
                
                #Sendto the Display 
                if MinidisplayOption: 
                    disp.displayFast(img)
                    
                    
                    
                if (takeimage ==1):                
                    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
                    img.save(name, format="png") 
                    takeimage = 0 
                    
                    
                #MOVE TO ALL OTHER INSTANCES 
                if (recordVideo == True):  
                    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))   
                    
                    
                    
            #end of scopemode 1 lobster mode 
                
            elif(Scope_mode == 2):  #settings menu 
                settingAdjustNumber = 0.000;
                BallisticThreader.thread.ScopeMode =2;  #not use ballistics in background when settings 
                BallisticThreader.thread.dt = 1
                BallisticThreader.thread.T = 2
                fpsBalls = BallisticThreader.thread.fpsaveout
            
            
                img.paste(image_settings,(0,0))
                
    
                # Read the Rotary Encoders for the Menu Input 
                
                if (SensorThreader.thread.encoder1Output !=  0 ):
                    menuNumber = menuNumber + (SensorThreader.thread.encoder1Output)
                    SensorThreader.thread.encoder1Output = 0
                
                if (menuNumber > 11):
                    menuNumber = 0
                    Scope_mode = 4
                elif (menuNumber < 0):
                    menuNumber = 0
                    
                
                
                if (SensorThreader.thread.encoder2Output !=  0 ):
                    if (menuNumber == 0):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0
                        SensorThreader.thread.encoder2Output = 0
                    elif (menuNumber == 1):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0.001
                        BallisticThreader.thread.caliber += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0                       
                    elif (menuNumber == 2):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                        BallisticThreader.thread.bullet_weight_grain += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0      
                    elif (menuNumber == 3):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                        
                        if (SensorThreader.thread.encoder2Output > 0):
                            BallisticThreader.thread.Gsolver = 7
                        elif (SensorThreader.thread.encoder2Output < 0):
                            BallisticThreader.thread.Gsolver = 1
                        SensorThreader.thread.encoder2Output = 0                          
                    elif (menuNumber == 4):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0.001
                        BallisticThreader.thread.bc7_box += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0   
                    elif (menuNumber == 5):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 25
                        BallisticThreader.thread.zerodistance += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0                          
                    #elif (menuNumber == 6):
                    #    settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                    #    if (SensorThreader.thread.encoder2Output > 0):
                    #        drawsubhashes = True
                    #        drawsubsubs  = True              
                    #    elif (SensorThreader.thread.encoder2Output < 0):
                    #        drawsubhashes = False
                    #        drawsubsubs  = False
                    #    SensorThreader.thread.encoder2Output = 0                              
                    elif (menuNumber == 6):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 5
                        BallisticThreader.thread.fps_box += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0    
                    elif (menuNumber == 7):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0.1
                        windspeederrr= BallisticThreader.thread.windspeed
                        windspeederrr += settingAdjustNumber
                        if (windspeederrr < 0):
                            windspeederrr = 0; 
                        BallisticThreader.thread.windspeed = windspeederrr; 
                        SensorThreader.thread.encoder2Output = 0                          
                    elif (menuNumber == 8):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 5
                        winder= BallisticThreader.thread.wind_head_deg
                        winder += settingAdjustNumber
                        if (winder > 360):
                            winder -= 360;
                        elif (winder < 0):
                            winder += 360;  
                        BallisticThreader.thread.wind_head_deg = winder        
                        SensorThreader.thread.encoder2Output = 0    
                    elif (menuNumber == 11):
                        if (SensorThreader.thread.encoder2Output > 0):
                            Scope_mode = 3; #start the FF adjust 
                        SensorThreader.thread.encoder2Output = 0                           

                
                
                
                ##### Code for inputs and state drawings here. Positional numer for highlighter.... 
                yposition=(27, 50, 75 ,98, 121, 146, 167, 216)
                
                
                
                
                #Draw current settings 
                #cailber
                MESSAGE = str("{:.3f}".format(BallisticThreader.thread.caliber))        
                draw.text((136, yposition[0]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                
                #weight
                MESSAGE = str(int(BallisticThreader.thread.bullet_weight_grain)  )    
                draw.text((136, yposition[1]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
    
                #G model  
                if (BallisticThreader.thread.Gsolver == 1):
                    draw.rectangle((148, yposition[2]-3, 148+25, yposition[2]+17), outline = (255, 255, 255))            
                elif (BallisticThreader.thread.Gsolver == 7):
                    draw.rectangle((180, yposition[2]-3, 180+25, yposition[2]+17), outline = (255, 255, 255)) 
    
    
                #BC      
                MESSAGE = str("{:.3f}".format(BallisticThreader.thread.bc7_box))        
                draw.text((136, yposition[3]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
    
                #Zero Distance       
                MESSAGE = str(int(BallisticThreader.thread.zerodistance))        
                draw.text((136, yposition[4]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                            
                #Velocity    
                MESSAGE = str("{:.1f}".format(BallisticThreader.thread.fps_box))      
                draw.text((136, yposition[5]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
            
                #Wind  
                MESSAGE = str("{:.1f}".format(BallisticThreader.thread.windspeed))    
                draw.text((136, yposition[6]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                #Wind direction  
                MESSAGE = str(int(BallisticThreader.thread.wind_head_deg)) + " d"    
                draw.text((190, yposition[6]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
             
                
                                 
        
                
                #Selector Code 
                if (menuNumber>0 and menuNumber<7):
                    draw.rectangle((130, yposition[menuNumber-1]-3, 230, yposition[menuNumber-1]+18), outline = (255, 0, 0))  #disp.width, disp.height
                    draw.rectangle((131, yposition[menuNumber-1]-2, 229, yposition[menuNumber-1]+17), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 7): 
                    draw.rectangle((130, yposition[6]-3, 180, yposition[6]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 8): 
                    draw.rectangle((180, yposition[6]-3, 230, yposition[6]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 9): 
                    draw.rectangle((10, yposition[7]-3, 80, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 10): 
                    draw.rectangle((90, yposition[7]-3, 160, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 11): 
                    draw.rectangle((172, yposition[7]-3, 225, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
        
            
            
            
            
            
            
                #Display on GUI 
                if BigdisplayOption:
                    show_frames(img)
                
                #Sendto the Display 
                if MinidisplayOption: 
                    disp.displayFast(img)        
            #end of scopemode 2 SETTINGS mode 
                if (takeimage ==1):                
                    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
                    img.save(name, format="png") 
                    takeimage = 0 
                    
                    
                #MOVE TO ALL OTHER INSTANCES 
                if (recordVideo == True):  
                    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
                    
            
            elif(Scope_mode == 3):  #Focal Length Calibration :) 

                pasteimage4 = CamThreader.thread.imageout # get new frame from thread 
                fpsCAM  = CamThreader.thread.fpsaveout  #grab the output 
                #pasteimage4.show() #FOR DEBUG ONLY DONT USE LOOPING OPENS WINDOW 
                pasteimage4=pasteimage4.resize((240,180),resample=Image.NEAREST) #BIG FPS nearest is fast  
 
                ####################################PIL IMAGE GENERATION#######################################              
                #Blank slate program. The ulimate tool for a master criminal trying to get a clean record 
                img.paste(blackframe,(0,0))
                
                
                ### Draw Camaera IMAGE
                img.paste(pasteimage4,(0,30))
                
                #######DrawZoomLevel
                
                #thezoom = int(1/CamThreader.thread.zoom)
                MESSAGE = str("{:.1f}".format(1/CamThreader.thread.zoom)) + "x" 
                draw.text((2,180), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))

                #Roatry Encoder
                
                ###### Focal Length LEVEL ADJUST 
                if (SensorThreader.thread.encoder1Output !=  0 ):
                    changeOpitcs = 1
                    focallength = focallength + ((SensorThreader.thread.encoder1Output)/4)
                    SensorThreader.thread.encoder1Output = 0
                 #######ZOOM LEVEL ADJUST    
                if (SensorThreader.thread.encoder2Output !=  0 ):
                    newzoom = CamThreader.thread.zoom/(pow(2,SensorThreader.thread.encoder2Output)) 
                    if (newzoom > 1.0):
                        CamThreader.thread.zoom = 1.0
                    elif (newzoom < 0.0625):
                        CamThreader.thread.zoom = 0.0625
                    else: 
                        CamThreader.thread.zoom = newzoom
                    SensorThreader.thread.encoder2Output = 0        
                
                if (changeOpitcs == 1 ):
                    opticres = 1 / ((math.atan(0.00155 / focallength)*57.295779513)*60)
                    opticPercent = opticres/3040  #was 3040 or 4056v 
                    changeOpitcs = 0                
                            
                ############# Draw Focal Length info 
                dirbox_h = 21
                dirbox_w = 78
                Yoffset = 8
                
                MESSAGE = "Focal Length:"  + "\nElev: " + str("{:.2f}".format(focallength)) + " mm"
                
                draw.rectangle((0, Yoffset, dirbox_w, Yoffset+dirbox_h), (0, 0, 0))  #disp.width, disp.height
                draw.text((5, Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                            
                ############# Draw MOA Solved DISPLAY 
                windbox_h = 31
                windbox_w = 63
                Yoffset = HEIGHT  - windbox_h - 3
                
                MESSAGE = "Press Button" + "\nTo Exit." 
                #MOA 
                draw.rectangle((WIDTH - windbox_w, Yoffset, WIDTH, Yoffset+windbox_h), (0, 0, 0))  #disp.width, disp.height
                draw.text((WIDTH - windbox_w, Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255))
                 
                ### Draw CrossHair
                
                #draw.rectangle((119, 117, 119, 121), (255, 0, 0))
                #draw.rectangle((117, 119, 121, 119), (255, 0, 0))  
                
                
                oneMoaScreen = opticres
                scaling = CamThreader.thread.zoom
            
                
                subhashcolor= (0,255,0)
                markercolor = (255,255,255)
                subsubcolor = (255,0,0)
            
                markeroffsetX = -scopexoffset
                markeroffsetY = -scopeyoffset
                
                
                
                #Horizontal Line and hashes 
                draw.rectangle((0, 119, 239, 119), (255, 0, 0))  
                
                #Veritical 
                #straight red line  :)  
                draw.rectangle((119, 30, 119, 209), (255, 0, 0))
                    
                drawsubhasesroutine(draw, scaling, subhashcolor, drawsubsubs, subsubcolor,markeroffsetX,markercolor, markeroffsetY) #############################################################
                ###########
 

                 
                #Display on GUI 
                if BigdisplayOption:
                    show_frames(img)
                
                #Sendto the Display 
                if MinidisplayOption: 
                    disp.displayFast(img)        
                #end of scopemode 3 FOCAL LENGHT ADJ   
                if (takeimage ==1):                
                    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
                    img.save(name, format="png") 
                    takeimage = 0 
                    
                    
                #MOVE TO ALL OTHER INSTANCES 
                if (recordVideo == True):  
                    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
                    
                ###################################################################################

            elif(Scope_mode == 4):  #settings menu 
                settingAdjustNumber = 0.000;
                BallisticThreader.thread.ScopeMode =2;  #not use ballistics in background when settings 
                BallisticThreader.thread.dt = 1
                BallisticThreader.thread.T = 2
                fpsBalls = BallisticThreader.thread.fpsaveout
            
            
                img.paste(image_settingsP2,(0,0))
                
    
                # Read the Rotary Encoders for the Menu Input 
                
                if (SensorThreader.thread.encoder1Output !=  0 ):
                    menuNumber = menuNumber + (SensorThreader.thread.encoder1Output)
                    SensorThreader.thread.encoder1Output = 0
                
                if (menuNumber > 6):
                    menuNumber = 6
                elif (menuNumber < 0):
                    menuNumber = 11
                    Scope_mode = 2 
                
                
                if (SensorThreader.thread.encoder2Output !=  0 ):
                    if (menuNumber == 0):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0
                        SensorThreader.thread.encoder2Output = 0
                    elif (menuNumber == 1):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 50
                        BallisticThreader.thread.Atm_altitude += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0                       
                    elif (menuNumber == 2):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0.25
                        BallisticThreader.thread.Atm_pressure += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0      
                    elif (menuNumber == 3):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                        BallisticThreader.thread.Atm_temperature += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0    
                         
                    elif (menuNumber == 4):
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 0.01
                        BallisticThreader.thread.Atm_RelHumidity += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0   
                    elif (menuNumber == 5): #latitude 
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                        #BallisticThreader.thread.zerodistance += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0                                                      
                    elif (menuNumber == 6): #longitude 
                        settingAdjustNumber = SensorThreader.thread.encoder2Output * 1
                        #BallisticThreader.thread.fps_box += settingAdjustNumber
                        SensorThreader.thread.encoder2Output = 0    
   

                
                
                
                ##### Code for inputs and state drawings here. Positional numer for highlighter.... 
                yposition=(27, 50, 75 ,98, 121, 146, 167, 216)
                
                
                
                
                #Draw current settings 
                #Altitude
                MESSAGE = str("{:.3f}".format(BallisticThreader.thread.Atm_altitude / 1000))      
                draw.text((136, yposition[0]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                
                #Pressure
                MESSAGE = str("{:.2f}".format(BallisticThreader.thread.Atm_pressure)  )    
                draw.text((136, yposition[1]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
    
                #Temperatre 
                MESSAGE = str(int(BallisticThreader.thread.Atm_temperature))        
                draw.text((136, yposition[2]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   

                #R. Humidity      
                MESSAGE = str(int(BallisticThreader.thread.Atm_RelHumidity*100)) + "%"       
                draw.text((136, yposition[3]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
    
                #Latitude       
                MESSAGE = str(39.73555)      #str(int(BallisticThreader.thread.zerodistance))        )
                draw.text((136, yposition[4]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
                            
                #Longitude   
                MESSAGE = str(104.98972) #str("{:.1f}".format(BallisticThreader.thread.fps_box))      
                draw.text((136, yposition[5]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
            
                
                                 
        
                
                #Selector Code 
                if (menuNumber>0 and menuNumber<7):
                    draw.rectangle((130, yposition[menuNumber-1]-3, 230, yposition[menuNumber-1]+18), outline = (255, 0, 0))  #disp.width, disp.height
                    draw.rectangle((131, yposition[menuNumber-1]-2, 229, yposition[menuNumber-1]+17), outline = (255, 0, 0))  #disp.width, disp.height

            
            
            
            
            
            
                #Display on GUI 
                if BigdisplayOption:
                    show_frames(img)
                
                #Sendto the Display 
                if MinidisplayOption: 
                    disp.displayFast(img)        
            #end of scopemode 2 SETTINGS mode 

                if (takeimage ==1):                
                    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
                    img.save(name, format="png") 
                    takeimage = 0 
                    
                    
                #MOVE TO ALL OTHER INSTANCES 
                if (recordVideo == True):  
                    video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

            
            #END STATE CALCULATIONS   
            
            t_end = time.time()
            
            fps = -1/(t_start - t_end)
            fpsave = fpsave + fps
            
            #check Mode Transisiton (above 35 deg angle of scope to transisiotn to Lobster Mode!  ) 
            
            if (Scope_mode != 2):
                if (Scope_mode == 0 and pitch_d > 40):
                    BallisticThreader.thread.solver = "Jacksolver"
                    print("Transitioning to LOBSTER")
                    #time.sleep(0.3)
                    Scope_mode = 1; 
                elif (Scope_mode == 1 and pitch_d < 40): 
                    BallisticThreader.thread.solver = ChooseSolver
                    #time.sleep(0.3)
                    print("Leaving LOBSTER")
                    Scope_mode = 0; 
            
            #print("Scope mode is " + str(Scope_mode))
            
    
            
        
        fpsavefr = fpsave/30#00 
        #print("Display: " + str("{:.2f}".format(fpsavefr)) + "  Ballisitcs: " + str("{:.2f}".format(fpsBalls)) + "  Camera:  " + str("{:.2f}".format(fpsCAM)) + "  Sensors:  " + str("{:.2f}".format(fpsSensor)))
        #print("CPU Temp is : " + str(cpu.temperature))
    
    
            
def drawsubhasesroutine(draw, scaling, subhashcolor, drawsubsubs, subsubcolor, markeroffsetX, markercolor,markeroffsetY):
        
    if (drawsubhashes):
        
        if (scaling < 0.125) :
        
        
            Marker= 1 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            Marker= 2 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 3 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 4 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
            Marker= 5 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 6 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)    
            
            Marker= 7 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            if drawsubsubs:     
                for Marker in range(8):                
                    xplace =  ( (Marker+1) * opticPercent ) * 180 /scaling
                    for i in range(6): 
    
                        draw.point(((119-xplace), 119+((i+1)*xplace/(Marker+1)) ), subsubcolor)
                        draw.point(((119+xplace), 119+((i+1)*xplace/(Marker+1)) ), subsubcolor)
                    
                
                
    
            
        
    
        elif (scaling >= 0.125 and scaling < 0.25):        
        
        
            Marker= 1 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
                
        
            Marker= 2 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 3 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 4 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
            Marker= 5 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 6 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)    
            
            Marker= 7 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 8 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 9 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 10 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
            Marker= 12 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)            
    
            #if drawsubsubs:     
            #    for Marker in range(8):                
            #        xplace = ( (Marker+1) * opticPercent ) * 180 /scaling
            #        for i in range(6): 
            #
            #            draw.point(((119-xplace), 119+((i+1)*xplace/(Marker+1)) ), subhashcolor)
            #            draw.point(((119+xplace), 119+((i+1)*xplace/(Marker+1)) ), subhashcolor)
    
        elif (scaling >= 0.25 and scaling < 0.5): 
        
            Marker= 5 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
                    
            Marker= 10 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 15 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)    
    
            
            Marker= 20 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)    
            
            Marker= 30 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 35 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)       

            Marker= 40 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 45 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)                
        
        elif (scaling >= 0.5 and scaling < 1.0): 
            Marker= 5 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)     
            
            Marker= 10 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            
            Marker= 15 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)        
            
            Marker= 20 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 30 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
    
            
            Marker= 35 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 40 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 45 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)   
            
        
            Marker= 50 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            
            Marker= 55 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)        
            
        elif (scaling == 1): 
            Marker= 5 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)     
            
            Marker= 10 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            
            Marker= 15 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)        
            
            Marker= 20 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            #draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            #draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 30 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 35 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 40 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 45 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)   
            
        
            Marker= 50 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            
            Marker= 55 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)        
            
            Marker= 60 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            #draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            #draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 65 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 70 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 75 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            
            Marker= 80 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str((Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str((Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
        
        
        
        #Veritical #Veritical #Veritical #Veritical #Veritical #Veritical 
        
        if (scaling < 0.125) :
        
            Marker= 1 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            Marker= 2 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 3 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            Marker= 4 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
            Marker= 5 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
        
        elif (scaling >= 0.125 and scaling < 0.25): 
            Marker= 1 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
        
        
            Marker= 2 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 3 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            Marker= 4 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
            Marker= 5 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            
            Marker= 6 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
            Marker= 7 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 8 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
            Marker= 9 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 1
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 10 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)        
        
        elif (scaling >= 0.25 and scaling < 0.5): 
        
            Marker= 5 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
                    
            Marker= 10 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 15 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor) 
    
            
            Marker= 20 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)

            Marker= 30 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 35 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor) 
            
        elif (scaling >= 0.5 and scaling < 1.0): 
            Marker= 5 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)     
            
            Marker= 10 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            
            Marker= 15 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)      
            
            Marker= 20 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 30 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            Marker= 35 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 40 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
    
        elif (scaling == 1):
            Marker= 5 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)     
            
            Marker= 10 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            
            Marker= 15 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)      
            
            Marker= 20 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            #draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            #draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 25 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 30 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
    
            
            Marker= 35 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            Marker= 40 #moa 
            yplace =- ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 45 #moa 
            yplace =  - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
        
            Marker= 50 #moa 
            yplace =  - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            
            
            Marker= 55 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)             
    
            Marker= 60 #moa 
            yplace =  - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            #draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            #draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
            Marker= 65 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)           
    
            Marker= 70 #moa 
            yplace =  - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            #draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            #draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)           
            
            Marker= 75 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)   
            
            Marker= 80 #moa 
            yplace =  - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 5
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)
            draw.text((119-sizeLong+11,119+yplace-5), str((Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str((Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)           
                        













    
    
#def UP_switch_callback(channel):
#    name= "Z_testImage27" + str(time.time()) + ".png" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+
#    img.save(name, format="png") 
#    print("Switch UP pressed.  Saving Image.")
#
#def DOWN_switch_callback(channel):
#
#    global Scope_mode
#    
#    if (Scope_mode !=2): 
#        Scope_mode  = 2 
#    else: 
#        Scope_mode  = 0
#    
#    print('Switch DOWN pressed, Setting Menu.')
#               
                
def DOWN_switch_callback(channel):  #######SNAPSHOT UP B1 

    global takeimage
    
    takeimage =1 

    print("BUTTON DOWN pressed")

def B2_switch_callback(channel):      ##### SETTUNG

    global Scope_mode, menuNumber
    
    if (Scope_mode == 0 or Scope_mode == 1): 
        Scope_mode  = 2 
        menuNumber = 0 
    elif(Scope_mode == 3): 
        Scope_mode  = 2
        menuNumber = 0
        CamThreader.thread.zoom = 1.0
    else: 
        #saveConfig
        savedata = np.array([[BallisticThreader.thread.caliber, BallisticThreader.thread.bullet_weight_grain, BallisticThreader.thread.Gsolver, BallisticThreader.thread.bc7_box, BallisticThreader.thread.zerodistance, BallisticThreader.thread.fps_box, BallisticThreader.thread.windspeed, BallisticThreader.thread.wind_head_deg,BallisticThreader.thread.Atm_altitude, BallisticThreader.thread.Atm_pressure, BallisticThreader.thread.Atm_temperature, BallisticThreader.thread.Atm_RelHumidity, focallength]])
        save("/home/pi/share/Display/configData.npy", savedata)
        
        #and leave the mode 
        Scope_mode  = 0
    
    print('BUTTON 2  pressed')      
    
def B3_switch_callback(channel):      ##### SETTUNG
    global takeimage, video, recordVideo
    
    takeimage =1 
    
    if (recordVideo == False): 
        #name= "VIDEO" + str(time.time()) + ".mp4" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+           
        name= "VIDEO" + str(time.time()) + ".avi" #str(time.time())  + str(time.time()) "/home/pi/savedscreenshots/"+           
        video = cv2.VideoWriter(name,fourcc, 29.9,(240,240))
        recordVideo = True ;
    else:
        recordVideo = False;
        video.release()
        
    
    
    print('BUTTON 3  pressed')        
                
def RIGHT_switch_callback(channel):      ##### SETTUNG

    global distance, focallength, changeOpitcs
    
    #changeOpitcs = 1
    #focallength += 0.5
    distance -= 25
    
    print('Switch RIGHT pressed')    


def LEFT_switch_callback(channel):      ##### SETTUNG

    global distance, focallength, changeOpitcs
    
    #changeOpitcs = 1
    #focallength -= 0.5
    distance += 25
    
    print('Switch LEFT pressed')   

def UP_switch_callback(channel):      ##### Zoom out  UP 
    
    zommer = CamThreader.thread.zoom *1.05  #+ 0.0625
    
    if (zommer > 1.0):
        zommer = 1.0
        
    CamThreader.thread.zoom = zommer  
    
    print('Switch UP pressed')  
    print("zoom is: " + str(CamThreader.thread.zoom))
    
def B1_switch_callback(channel):      ##### Zoom in 


    
 
    #CamThreader.thread.zoom = CamThreader.thread.zoom  / 1.05  #- 0.0625  
    global printNow, LaserOn
    
    #if (Scope_mode == 0 and BallisticThreader.thread.printerGO == False):
    #    if (printNow == False ):
    #        printNow =True; 
    #        BallisticThreader.thread.printerGO = printNow
    #        printNow =False;
    #        print('Button 1 pressed, Printing.')
    #        
    

    
    if (Scope_mode == 0 and BallisticThreader.thread.Lasering == False):
        if (LaserOn == False ):
            LaserOn = True; 
            BallisticThreader.thread.Lasering = LaserOn
            LaserOn = False;
            print('Button 1 pressed, Lasering.')        
            
            
           
    
    
def CENTER_switch_callback(channel):      ##### SETTUNG

    
    print('Switch CENTER pressed')        
    
                                
#Button Definning :))focallength
###J_UP = 6
###J_DOWN = 19
###J_LEFT = 5
###J_RIGHT = 26
###J_CENTER = 13
###J_1 = 21
###J_2 = 20
###J_3 = 16


#littleDisplay: 
###J_1 = 24
###J_2 = 23
###J_3 = 27

GPIO.add_event_detect(J_1, GPIO.RISING, callback=B1_switch_callback)     
GPIO.add_event_detect(J_2, GPIO.RISING, callback=B2_switch_callback)  
GPIO.add_event_detect(J_3, GPIO.RISING, callback=B3_switch_callback)   
 
#GPIO.add_event_detect(J_UP, GPIO.RISING, callback=UP_switch_callback)     
#GPIO.add_event_detect(J_DOWN, GPIO.RISING, callback=DOWN_switch_callback)  
#GPIO.add_event_detect(J_LEFT, GPIO.RISING, callback=LEFT_switch_callback)     
#GPIO.add_event_detect(J_RIGHT, GPIO.RISING, callback=RIGHT_switch_callback)    
#GPIO.add_event_detect(J_CENTER, GPIO.RISING, callback=CENTER_switch_callback)      
            

# Repeat after an interval to capture continiously
if __name__ == "__main__":
    print("Starting Program :) ")
    #Scope_mode = 999999
    #print(Scope_mode)
    main()


  

