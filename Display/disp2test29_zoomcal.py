#Display? 
MinidisplayOption =  True  

BigdisplayOption = False   #False  True 

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

import CamThreader 

#import SensorThreader 

import BallisticThreaderAdvancedExtension    as BallisticThreader

import RPi.GPIO as GPIO 

#########MEasure Temp       vcgencmd measure_temp

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
#J_UP = 23
#J_DOWN = 24
#GPIO.setup(J_UP, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_UP) 


J_UP = 6
J_DOWN = 19
J_LEFT = 5
J_RIGHT = 26
J_CENTER = 13
J_1 = 21
J_2 = 20
J_3 = 16

GPIO.setup(J_UP, GPIO.IN,pull_up_down=GPIO.PUD_UP) ######buttons so you dont short shit lol 
GPIO.setup(J_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_LEFT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_RIGHT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_CENTER,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_3, GPIO.IN,pull_up_down=GPIO.PUD_UP) 



 
 
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



 
#st77789 
disp=ST7789.ST7789(height=240, width=240, port=0,rst = 27, cs=0,dc=25,backlight=24,rotation=180,spi_speed_hz=62500*1000)   #dc5 160000000 48000000
disp._spi.mode=3  
disp.reset()  
disp._init()  
#image=Image.new('RGB',(240,240),(255,0,0))  #('RGB',(240,240),(r,g,b))
#display.display(image)  
#sleep(2)  
#mode directory here: /usr/local/lib/python3.7/dist-packages/ST7789  



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

sleep(3)

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

image_settings=Image.open("/home/pi/share/Display/SettingsMenuBase3.jpg") 


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


distance = 485.0
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
CamThreader.thread.zoom = 1.0
zoomtest = False
zoomtester = 0
zoomincrease = 1 

sleep(1)



#Mode Tester! 
Scope_mode = 0  #0 main   1 Lobster    2 Settings 
modecounter = 0 
modecycletest = False

#Crosshairs 
drawsubhashes = True

#Drawsubsubs 
drawsubsubs  = True


#menu fo the settings 
menuNumber= 0;

#needed hard 
focallength = 103 #mm ########OHHHH THIS IS SHITTY 

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



CamThreader.thread.clicky   = int(scopeyoffset  * opticres)
CamThreader.thread.clicky   = int(scopeyoffset  * opticres) 




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
    global Scope_mode, zoomtester, dropcounter, fpsavefr, flash, zoomincrease, menuNumber, takeimage,focallength,opticPercent,opticres, changeOpitcs
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
            head = 0#SensorThreader.thread.output_heading
            pitch =0# -SensorThreader.thread.pitch
            roll = 0#SensorThreader.thread.roll
            fpsSensor  = 0# SensorThreader.thread.fpsaveout
            pitch_d = pitch * 57.2957795;
            
            if (changeOpitcs ==1 ):
                opticres = 1 / ((math.atan(0.00155 / focallength)*57.295779513)*60)
                opticPercent = opticres/3040
                changeOpitcs = 0
            
            
            if ( Scope_mode == 0):   #0 is regular scope #1 is LOBSTER mode 
                BallisticThreader.thread.ScopeMode =0;
                BallisticThreader.thread.dt = 0.05
                BallisticThreader.thread.T = 3
            
            
            
                pasteimage4 = CamThreader.thread.imageout # get new frame from thread 
                fpsCAM  = CamThreader.thread.fpsaveout  #grab the output 
                #pasteimage4.show() #FOR DEBUG ONLY DONT USE LOOPING OPENS WINDOW 
                pasteimage4=pasteimage4.resize((240,180),resample=Image.NEAREST) #BIG FPS nearest is fast 
                
                
                #Calculate States Simulation for fake data on screen    
                
                
                
                #correct the bullshit math i cant figure out.... 
                if (CamThreader.thread.zoom > (1/2.0)): #2.9
                    scopexoffset = 0   #angle right 20  MOA 
                    scopeyoffset = 0 #angle up 40 MOA 
                    CamThreader.thread.clickx   = int(scopexoffset  * opticPercent* 2028)     #for Mode 1 camera 
                    CamThreader.thread.clicky   = int(scopeyoffset  * opticPercent* 2028)               
                else: 
                    scopexoffset = inputXShift  #angle right 20  MOA 
                    scopeyoffset = inputYShift                  #angle up 40 MOA 
                    CamThreader.thread.clickx   = int(scopexoffset  * opticPercent* 2028)
                    CamThreader.thread.clicky   = int(scopeyoffset  * opticPercent * 2028)
                    #print(CamThreader.thread.clicky)
                
                
                
                
                
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
                distance = 143 # Lasered,  will update later yds
                distance_m = distance * 0.9144;
                fakewindspeed = 0 #mph 
                fakewindheading = 90 #deg (east)
                    
                
            
                
                #inputs 
                startheight  = 0 #meters 
                
                
                #From Sensor Thread, Always updating in backgorund 
                #head = SensorThreader.thread.output_heading
                #pitch = -SensorThreader.thread.pitch #- 0.01308997
                #roll = SensorThreader.thread.roll
                #fpsSensor  = SensorThreader.thread.fpsaveout
                
                wobbleY = 0#SensorThreader.thread.wobbleY
                wobbleX = 0#SensorThreader.thread.wobbleX
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
                BallisticThreader.thread.windspeed = fakewindspeed
                BallisticThreader.thread.wind_head_deg = fakewindheading
                
                
                fpsBalls = BallisticThreader.thread.fpsaveout
                
                solution = BallisticThreader.thread.solution
                plot = BallisticThreader.thread.plotter
                
                
            
                
                
                
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
                impactzoneX = - ( (windmoa + scopexoffset) * opticPercent ) * 180 /scaling;
                
    
                
                
                
                
                
                ####################################PIL IMAGE GENERATION#######################################
                
                #Blank slate program. The ulimate tool for a master criminal trying to get a clean record 
                img.paste(blackframe,(0,0))
                
                
                ### Draw Camaera IMAGE
                img.paste(pasteimage4,(0,30))
                
                
                
                ##############WIND DISPLAYING  
                
                
                windbox_h = 21
                windbox_w = 78
                Yoffset = 8
                
                MESSAGE = "Wind: " + str("{:.2f}".format(wind)) + " mph"  + "\n FPS: " + str("{:.2f}".format(fpsavefr))  + " deg"
                
                draw.rectangle((239-windbox_w, Yoffset, 239, Yoffset+windbox_h), (0, 0, 0))  #disp.width, disp.heigh
                draw.text((239-windbox_w,Yoffset), MESSAGE, spacing = 1, font=font, fill=(255, 255, 255))
                
                
                #######DrawZoomLevel
                
                #thezoom = int(1/CamThreader.thread.zoom)
                MESSAGE = str("{:.1f}".format(1/CamThreader.thread.zoom)) + "x" 
                draw.text((2,180), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                
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
                
                MESSAGE = "MOA SOLVED:" + "\nFF: " + str("{:.2f}".format(focallength)) + "\nElev: " + str("{:.2f}".format(dropmoa)) 
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
                
                
                
                MESSAGE = "   V " + "\n" +str("{:.2f}".format(pos))  
                
                draw.rectangle((107,Yoffset,107+compbox_h+20 ,compbox_w + Yoffset-11), (0, 0, 0))  #disp.width, disp.height
                draw.text((107,Yoffset), MESSAGE, font=fontL, spacing = 1, fill=(255, 255, 255)) #int(text_x), int(text_y)  
                
                
                
                
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
            
            
                
                
                
                ###Draw Stability Marker 
                
                indicatorcolor = (0,0,255) #blue 
                
                #print(indicatorcolor)
                centerx = 119 + impactzoneX
                centery = 119 + impactzoneY
                r = (wobble_radius*wobble_radius)/10
                shape = [((centerx-wobble_radius),(centery-wobble_radius)),((centerx+wobble_radius) , (centery+wobble_radius))]
                draw.arc(shape, start =0 , end = 360 , fill = indicatorcolor)
            
                
                ####Draw the Plot at bottom using Paste Function 
                img.paste(plot,(0,240-30))    
    
                
                
                
                
                
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
    
    
                
            
            
            elif (Scope_mode == 1):   #LOBSTER MODE 
                BallisticThreader.thread.ScopeMode =1;    #Scope_mode
                BallisticThreader.thread.dt = 2
                BallisticThreader.thread.T = 60
                
                img.paste(image_lob,(0,0))
                
                #draw.rectangle((0,0,239,239), (0, 0, 0))  #disp.width, disp.height  #not needed. keep for reference later? 
                
                #img.paste(blackframe,(0,0))  
    
                #############################    BALLISTICS CALCULATION ################################
                distance = 500 # Lasered,  will update later yds
                distance_m = distance * 0.9144;
                
                target_elevation =  math.radians(10) # degrees to rads  ########### TODO NOT IMPLEMENTED YET 
                
            
                
                #inputs 
                startheight  = 0 #meters 
                
                
                #From Sensor Thread, Always updating in backgorund 
                #head = SensorThreader.thread.output_heading
                #pitch = -SensorThreader.thread.pitch
                #roll = SensorThreader.thread.roll
                #fpsSensor  = SensorThreader.thread.fpsaveout
                
                wobbleY = 0#SensorThreader.thread.wobbleY
                wobbleX = 0#SensorThreader.thread.wobbleX
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
                BallisticThreader.thread.targetdistin =  distance_m
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
            
                
            elif(Scope_mode == 2):  #settings menu 
                BallisticThreader.thread.ScopeMode =2;  #not use ballistics in background when settings 
                BallisticThreader.thread.dt = 1
                BallisticThreader.thread.T = 2
                fpsBalls = BallisticThreader.thread.fpsaveout
            
            
                img.paste(image_settings,(0,0))
                
    
                
                if (menuNumber > 10):
                    menuNumber = 0
                
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
                            
                #Reticle    
                MESSAGE = "MOA"       
                draw.text((136, yposition[5]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
            
                #Reticle    
                MESSAGE = ChooseSolver      
                draw.text((136, yposition[6]), MESSAGE, spacing = 1, font=SettingsFont, fill=(255, 255, 255)) #int(text_x), int(text_y)   
            
                
                
                
                #Selector Code 
                if (menuNumber>0 and menuNumber<8):
                    draw.rectangle((130, yposition[menuNumber-1]-3, 230, yposition[menuNumber-1]+18), outline = (255, 0, 0))  #disp.width, disp.height
                    draw.rectangle((131, yposition[menuNumber-1]-2, 229, yposition[menuNumber-1]+17), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 8): 
                    draw.rectangle((10, yposition[7]-3, 80, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 9): 
                    draw.rectangle((90, yposition[7]-3, 160, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
                elif(menuNumber == 10): 
                    draw.rectangle((172, yposition[7]-3, 225, yposition[7]+18), outline = (255, 0, 0))  #disp.width, disp.height
        
            
            
            
            
            
            
                #Display on GUI 
                if BigdisplayOption:
                    show_frames(img)
                
                #Sendto the Display 
                if MinidisplayOption: 
                    disp.displayFast(img)        
            
    
            
            #END STATE CALCULATIONS   
            
            t_end = time.time()
            
            fps = -1/(t_start - t_end)
            fpsave = fpsave + fps
            
            #check Mode Transisiton (above 35 deg angle of scope to transisiotn to Lobster Mode!  ) 
            
            if (Scope_mode != 2):
                if (pitch_d > 38.0):
                    BallisticThreader.thread.solver = "Jacksolver"
                    #time.sleep(0.3)
                    Scope_mode = 1; 
                else: 
                    BallisticThreader.thread.solver = ChooseSolver
                    #time.sleep(0.3)
                    Scope_mode = 0; 
                
            
    
            
        
        fpsavefr = fpsave/30#00 
        print("Display: " + str("{:.2f}".format(fpsavefr)) + "  Ballisitcs: " + str("{:.2f}".format(fpsBalls)) + "  Camera:  " + str("{:.2f}".format(fpsCAM)) + "  Sensors:  " + str("{:.2f}".format(fpsSensor)))
        #print("Heading: " + str("{:.2f}".format(head)) + "  Pitch_:  " + str("{:.2f}".format(pitch_d)) + "  Roll:  " + str("{:.2f}".format(roll)))
        
        #print("Camera:  " + str("{:.2f}".format(fpsCAM)))    # "{:.2f}".format(
        #looper= False;
    
    
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)    
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)    
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)   
    
            Marker= 12 #moa 
            xplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-xplace, 119-sizeLong), (119-xplace, 119+sizeLong)], subhashcolor)
            draw.line([(119+xplace, 119-sizeLong), (119+xplace, 119+sizeLong)], subhashcolor)
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)            
    
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119+xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker + markeroffsetX)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-xplace-5,119-sizeLong+11), str("{:.1f}".format(Marker - markeroffsetX)), font=font, spacing = 1, fill=markercolor)
        
        
        
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
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
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
    
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)        
        
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
    
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            
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
            draw.text((119-sizeLong+11,119+yplace-5), str("{:.1f}".format(Marker + markeroffsetY)), font=font, spacing = 1, fill=markercolor)
            draw.text((119-sizeLong+11,119-yplace-5), str("{:.1f}".format(Marker - markeroffsetY)), font=font, spacing = 1, fill=markercolor)           
            
            Marker= 75 #moa 
            yplace = - ( (Marker) * opticPercent ) * 180 /scaling
            sizeLong = 2
            draw.line([(119-sizeLong, 119-yplace), (119+sizeLong, 119-yplace)], subhashcolor)
            draw.line([(119-sizeLong, 119+yplace), (119+sizeLong, 119+yplace)], subhashcolor)   
            













    
    
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
                
def B1_switch_callback(channel):  #######SNAPSHOT

    global takeimage
    
    takeimage =1 
    
    print("BUTTON 1 pressed")

def B2_switch_callback(channel):      ##### SETTUNG

    global Scope_mode
    
    if (Scope_mode !=2): 
        Scope_mode  = 2 
    else: 
        Scope_mode  = 0
    
    print('BUTTON 2  pressed')      
    
def B3_switch_callback(channel):      ##### SETTUNG

    
    print('BUTTON 3  pressed')        
                
def RIGHT_switch_callback(channel):      ##### SETTUNG

    global focallength, changeOpitcs
    
    changeOpitcs = 1
    focallength += 0.5
    
    print('Switch RIGHT pressed')    


def LEFT_switch_callback(channel):      ##### SETTUNG

    global focallength, changeOpitcs
    
    changeOpitcs = 1
    focallength -= 0.5
    
    print('Switch LEFT pressed')   

def UP_switch_callback(channel):      ##### SETTUNG
    
    CamThreader.thread.zoom = CamThreader.thread.zoom *1.05  #+ 0.0625
    
    print('Switch UP pressed')   
    
def DOWN_switch_callback(channel):      ##### SETTUNG
 
    CamThreader.thread.zoom = CamThreader.thread.zoom  / 1.05  #- 0.0625
    
    print('Switch DOWN pressed')       
    
    
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
###J_UP = 23
###J_DOWN = 24

 
GPIO.add_event_detect(J_UP, GPIO.RISING, callback=UP_switch_callback)     
GPIO.add_event_detect(J_DOWN, GPIO.RISING, callback=DOWN_switch_callback)  
GPIO.add_event_detect(J_LEFT, GPIO.RISING, callback=LEFT_switch_callback)     
GPIO.add_event_detect(J_RIGHT, GPIO.RISING, callback=RIGHT_switch_callback)  
GPIO.add_event_detect(J_1, GPIO.RISING, callback=B1_switch_callback)     
GPIO.add_event_detect(J_2, GPIO.RISING, callback=B2_switch_callback)  
GPIO.add_event_detect(J_3, GPIO.RISING, callback=B3_switch_callback)     
GPIO.add_event_detect(J_CENTER, GPIO.RISING, callback=CENTER_switch_callback)      
            

# Repeat after an interval to capture continiously
if __name__ == "__main__":
    print("Starting Program :) ")
    #Scope_mode = 999999
    #print(Scope_mode)
    main()


  

