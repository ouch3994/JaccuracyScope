#Display? 
MinidisplayOption =  True

BigdisplayOption = False #False  True 

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

#import SensorThreaderSlowerRotaryEncodersTRY as SensorThreader 

#import BallisticThreaderAdvancedExtension    as BallisticThreader

import RPi.GPIO as GPIO 

from gpiozero import CPUTemperature

from numpy import load
from numpy import save


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
#J_1 = 23
#J_2 = 24
#GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#print("buttons setup...")


#J_UP = 6
#J_DOWN = 19
#J_LEFT = 5
#J_RIGHT = 26
#J_CENTER = 13
#J_1 = 21
#J_2 = 20
#J_3 = 16

#GPIO.setup(J_UP, GPIO.IN,pull_up_down=GPIO.PUD_UP) ######buttons so you dont short shit lol 
#GPIO.setup(J_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_LEFT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_RIGHT, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_CENTER,GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
#GPIO.setup(J_3, GPIO.IN,pull_up_down=GPIO.PUD_UP) 


cpu = CPUTemperature()
 
 
if BigdisplayOption:
    # Create an instance of TKinter Window or frame
    win = Tk()
    win.bind('<Escape>', lambda e: app.quit())
    
    # Set the size of the window
    #win.geometry("240x240")
    win.geometry("240x240")
    
    # Create a Label to capture the Video frames
    label =Label(win)
    label.grid(row=0, column=0)
    label.configure(bg='black')



 
#st77789  backlight=24,rotation=180
disp=ST7789.ST7789(height=240, width=240, port=0,rst = 27, cs=0,dc=25,backlight=24,rotation=90,spi_speed_hz=78*1000*1000)   #dc5 62500*1000 62500000 160000000 48000000
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
    img2x=img.resize((240,240),resample=Image.NEAREST) 
    imgtk = dingerr.PhotoImage(image = img2x)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.update()  

sleep(2)



#disp.set_window(x0=0, y0=0, x1=10, y1=10)
blackframe = Image.new('RGB', (240, 240), color=(0, 0, 0))
img = Image.new('RGB', (240, 240), color=(0, 0, 0))
disp.display(img,xs=0,xe=239,ys=0,ye=239) #gotta match draw dimensions 
draw = ImageDraw.Draw(img)
#disp.display(img,xs=0,xe=0,ys=239,ye=239)


if BigdisplayOption:
    # Convert image to PhotoImage
    img2x=img.resize((240,240),resample=Image.NEAREST) 
    imgtk = dingerr.PhotoImage(image = img2x)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.update() 



image2=Image.open("/home/pi/share/Display/COMPASS4.jpg")   
image2=image2.resize((180,7),resample=Image.LANCZOS)


image_lob=Image.open("/home/pi/share/Display/lobstermodebase2.jpg")   

image_settings=Image.open("/home/pi/share/Display/SettingsMenuBase5.jpg") 


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
drawsubhashes = False

#Drawsubsubs 
drawsubsubs  = False


#menu fo the settings 
menuNumber= 0;
settingAdjustNumber = 0.000; 

#needed hard 
focallength = 77.25 #mm ########OHHHH THIS IS SHITTY    #.75 facto roff... try 77.25 not 103 

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


debounce = False; 
debouncer = 0 



CamThreader.thread.clicky   = int(scopeyoffset  * opticres)
CamThreader.thread.clicky   = int(scopeyoffset  * opticres) 




def show_frames(imger):
   # Get the latest frame and convert into Image


   # Convert image to PhotoImage
   imger2x=imger.resize((240,240),resample=Image.NEAREST) 
   imgtk = dingerr.PhotoImage(image = imger2x)
   #label.imgtk = imgtk
   label['image']=imgtk
   # Repeat after an interval to capture continiously
   label.update()

   











def main(): 
    global Scope_mode, zoomtester, dropcounter,distance,debouncer, debounce, drawsubhashes, drawsubsubs, fpsavefr, settingAdjustNumber, menuNumber,inputXShift, inputYShift, scopeyoffset,scopexoffset, flash, zoomincrease, menuNumber, takeimage,focallength,opticPercent,opticres, changeOpitcs
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
            head = 0
            pitch = 0
            roll = 0
            fpsSensor  = 0
            pitch_d = pitch * 57.2957795;
            
            if (changeOpitcs ==1 ):
                opticres = 1 / ((math.atan(0.00155 / focallength)*57.295779513)*60)
                opticPercent = opticres/3040  #was 3040 or 4056v 
                changeOpitcs = 0
            
            
            if ( Scope_mode == 0):   #0 is regular scope #1 is LOBSTER mode 

            
            
            
                pasteimage4 = CamThreader.thread.imageout # get new frame from thread 
                fpsCAM  = CamThreader.thread.fpsaveout  #grab the output 
                #pasteimage4.show() #FOR DEBUG ONLY DONT USE LOOPING OPENS WINDOW 
                
                #try this commented.... 
                #pasteimage4=pasteimage4.resize((240,180),resample=Image.NEAREST) #BIG FPS nearest is fast 
                
                
                        


                if(debounce == True): 
                    debouncer += 1
                    #print("debouncing....")
                    if (debouncer  > 10): 
                        debounce = False;
                        debouncer = 0;
                
                
                
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
                #distance = 125 # Lasered,  will update later yds
                distance_m = distance * 0.9144;
            
                
    
                
                #Apply scaling of camera to droppixels 
                scaling = CamThreader.thread.zoom
                
             
             
                
                
                
                
                ####################################PIL IMAGE GENERATION#######################################
                
                #Blank slate program. The ulimate tool for a master criminal trying to get a clean record 
                img.paste(blackframe,(0,0))
                
                
                ### Draw Camaera IMAGE
                img.paste(pasteimage4,(0,30))
                
                
                
                ##############WIND DISPLAYING  
                
                
                windbox_h = 21
                windbox_w = 78
                Yoffset = 8
                #replaced Wind with CPUtemp... put back to wind later...(mph)
                MESSAGE = "Temp: " + str("{:.2f}".format(cpu.temperature)) + " F"  + "\n FPS: " + str("{:.2f}".format(fpsavefr))  + " fps"
                
                draw.rectangle((239-windbox_w, Yoffset, 239, Yoffset+windbox_h), (0, 0, 0))  #disp.width, disp.heigh
                draw.text((239-windbox_w,Yoffset), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                
                
                #######DrawZoomLevel
                
                #thezoom = int(1/CamThreader.thread.zoom)
                MESSAGE = str("{:.1f}".format(1/CamThreader.thread.zoom)) + "x" 
                draw.text((2,180), MESSAGE, spacing = 1, font=fontL, fill=(255, 255, 255))
                


                
                oneMoaScreen = opticres
                
            
                
                subhashcolor= (0,255,0)
                markercolor = (255,255,255)
                subsubcolor = (255,0,0)
            
                markeroffsetX = -scopexoffset
                markeroffsetY = -scopeyoffset
                
                
                
                #Horizontal Line and hashes 
                #draw.rectangle((0, 119, 239, 119), (255, 0, 0))  
                
                #Veritical 
                #straight red line  :)  
                #draw.rectangle((119, 30, 119, 209), (255, 0, 0))
                    
                #drawsubhasesroutine(draw, scaling, subhashcolor, drawsubsubs, subsubcolor,markeroffsetX,markercolor, markeroffsetY) #############################################################
                ###################################################################################
                

            
                
              
                
                
                
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
                    
                    
                #END STATE CALCULATIONS   
            
                t_end = time.time()
                
                fps = -1/(t_start - t_end)
                fpsave = fpsave + fps
                        
                    
                    
                    
                    
                    
                    
    
        fpsavefr = fpsave/30#00 
        #print("Display: " + str("{:.2f}".format(fpsavefr)) + "  Ballisitcs: " + str("{:.2f}".format(fpsBalls)) + "  Camera:  " + str("{:.2f}".format(fpsCAM)) + "  Sensors:  " + str("{:.2f}".format(fpsSensor)))
        print("CPU Temp is : " + str(cpu.temperature))
    
    
            
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


    
    print('BUTTON 2  pressed')      
    
def B3_switch_callback(channel):      ##### SETTUNG

    
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

def DOWN_switch_callback(channel):      ##### Zoom out 
    
    zommer = CamThreader.thread.zoom *1.05  #+ 0.0625
    
    if (zommer > 1.0):
        zommer = 1.0
        
    CamThreader.thread.zoom = zommer  
    
    print('Switch UP pressed')  
    print("zoom is: " + str(CamThreader.thread.zoom))
    
def UP_switch_callback(channel):      ##### Zoom in 
 
    CamThreader.thread.zoom = CamThreader.thread.zoom  / 1.05  #- 0.0625  
    
    print('Switch DOWN pressed')       
    print("zoom is: " + str(CamThreader.thread.zoom))
    
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
###J_2 = 24

 
#GPIO.add_event_detect(J_UP, GPIO.RISING, callback=UP_switch_callback)     
#GPIO.add_event_detect(J_DOWN, GPIO.RISING, callback=DOWN_switch_callback)  
#GPIO.add_event_detect(J_LEFT, GPIO.RISING, callback=LEFT_switch_callback)     
#GPIO.add_event_detect(J_RIGHT, GPIO.RISING, callback=RIGHT_switch_callback)  




###Little Display 
J_1 = 23
J_2 = 24
GPIO.setup(J_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(J_2, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
print("buttons setup...")


GPIO.add_event_detect(J_1, GPIO.RISING, callback=UP_switch_callback)   #B1_switch_callback    
GPIO.add_event_detect(J_2, GPIO.RISING, callback=DOWN_switch_callback)    #B2_switch_callback
#GPIO.add_event_detect(J_3, GPIO.RISING, callback=B3_switch_callback)     
#GPIO.add_event_detect(J_CENTER, GPIO.RISING, callback=CENTER_switch_callback)      
#            

# Repeat after an interval to capture continiously
if __name__ == "__main__":
    print("Starting Program :) ")
    #Scope_mode = 999999
    #print(Scope_mode)
    main()


  

