import ST7789  
import math
from threading import Thread 
import numpy as np
import time 
from PIL import Image  



class DisplayThread(Thread): 

    def __init__(self): 
    
        Thread.__init__(self)
        
        #initial Display Setup! 
        self.disp=ST7789.ST7789(height=240, width=240, port=0, cs=0,dc=25,backlight=22,spi_speed_hz=62500*1000)   #dc5 160000000 48000000
        self.disp._spi.mode=3  
        self.disp.reset()  
        self.disp._init()  
        
        WIDTH = 240 #disp.width
        HEIGHT = 240 #disp.height
        
        ##disp.set_window(x0=0, y0=0, x1=239, y1=239)
        self.TESTimage=Image.open("TestGUIblank.jpg")  
        self.TESTimage=self.TESTimage.resize((240,240),resample=Image.NEAREST) 
        
        
        
        
        
        self.inputimg=Image.open("TestGUIblank.jpg")  
        self.inputimg=self.inputimg.resize((240,240),resample=Image.NEAREST) 
        self.disp.display(self.inputimg,xs=0,xe=239,ys=0,ye=239)
        
        #img = Image.new('RGB', (240, 240), color=(0, 0, 0)) #Blank frame incase needed for later 
        
        time.sleep(0.5)
        
        self.MafVal = 3
        self.fpsaveout = 0
        
        
        self.ready = 3
        
        self.getting  = 0
       
    
        
        
    def run(self):
        self.ready = 0
        while True: 
            
            
            #self.val1 = self.val1 +1 

            
            
            #Get a frame : 
            fpsave=0 
            
                  
            
            #moving Average Filter 
            for i in range (1,self.MafVal+1,1): 
            
                t_start = time.time()
                
                
                #only run this for absolute speeeeed 
                
                #loadimage = self.TESTimage # self.inputimg
                    
                loadimage = self.inputimg 
                
                self.disp.displayFast(loadimage)
                time.sleep(0.01)
                
                
                t_end = time.time()
                fps = -1/(t_start - t_end)
                fpsave = fpsave + (fps/self.MafVal)                    
                
                
                
                
                
                
                #time.sleep(1)


                
                
            #fpsave = fpsave/20
            self.fpsaveout = fpsave
            
            
            #print(self.pitchmaker)

            
            
            



            
thread = DisplayThread()
thread.start()

