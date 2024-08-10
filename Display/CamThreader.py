from picamera2 import Picamera2, Preview
from threading import Thread 
import numpy as np
from PIL import Image  #need ? 
from time import sleep
import time 


class CameraThread(Thread): 

    def __init__(self): 
    
        Thread.__init__(self)
        
        
        self.val1 = 1
        self.clickx = 0
        self.clicky = 0 
        self.clickxOld = 0
        self.clickyOld = 0 
        
        self.val1 = 1
        self.zoom = 1.0; 
        self.zoomold = 1.0; 
        
        #initial Camera Setup! 
        #instantiate the processes
        self.camera = Picamera2()
        preview_config = self.camera.create_preview_configuration(main = {"size": (240, 180)}, raw = self.camera.sensor_modes[2]) #(240, 180) (480, 360) (620, 480)
        
        #sensor Mode 2  = use 3040 as full height 
        #Sensor mode 1, use 1080 as full height 
        
        #print(preview_config)
        self.camera.configure(preview_config)
        
        print("Starting Camera...")
        self.camera.start()
        
        #self.camera.framerate = 30
        self.camera.rotation = 90
        
        time.sleep(1)
        
        self.OGsize = self.camera.capture_metadata()['ScalerCrop'][2:]
        self.full_res = self.camera.camera_properties['PixelArraySize']
        self.camera.capture_metadata()
        
        #mode zero limits 'crop_limits': (696, 528, 2664, 1980) 
        size = [int(s * self.zoom) for s in self.OGsize]   #0.0625
        offset = [(r - s) // 2 for r, s in zip(self.full_res, size)] 
        self.camera.set_controls({"ScalerCrop": offset + size , "FrameRate": (45), "Sharpness": (16)}) #, "AnalogueGain": 2.0
                
        
        self.fpsaveout = 0
        
        
        #Create the variables needed 
        
        
        
        
        
        
        
    def run(self):
        
        while True: 
            #sleep(.1)
            
            #self.val1 = self.val1 +1

            
            #Get a frame : 
            fpsave=0 
            
            for i in range (1,30,1): 
                t_start = time.time()
                
                (buffer, ), metadata = self.camera.capture_buffers(["main"])

                self.imageout = self.camera.helpers.make_image(buffer, self.camera.camera_configuration()["main"])   

                #print(self.camera.capture_metadata()['ScalerCrop'][2:])


                if ( self.zoom != self.zoomold or self.clickx != self.clickxOld or self.clicky != self.clickyOld):
                    #mode zero limits 'crop_limits': (696, 528, 2664, 1980) 
                    size = [int(s * self.zoom) for s in self.OGsize]   #0.0625
                    offset = [(r - s) // 2 for r, s in zip(self.full_res, size)] 
                    offset[0] = offset[0] + self.clickx 
                    offset[1] = offset[1] + self.clicky 
                    self.camera.set_controls({"ScalerCrop": offset + size })# , "FrameRate": (45)})
                    self.zoomold = self.zoom
                    self.clickxOld = self.clickx
                    self.clickyOld = self.clicky
                    #print("ZOOMING" + str(self.zoom))
 


 
                #if ( self.clickx != self.clickxOld):
                #    #mode zero limits 'crop_limits': (696, 528, 2664, 1980) 
                #    size = [int(s * self.zoom) for s in self.OGsize]   #0.0625
                #    offset = [(r - s) // 2 for r, s in zip(self.full_res, size)] 
                #    offset[0] = offset[0] + self.clickx 
                #    self.camera.set_controls({"ScalerCrop": offset + size , "FrameRate": (45)})
                #    self.clickxOld = self.clickx
                #    #print("ZOOMING" + str(self.zoom))    
                #
                #if ( self.clicky != self.clickyOld):
                #    #mode zero limits 'crop_limits': (696, 528, 2664, 1980) 
                #    size = [int(s * self.zoom) for s in self.OGsize]   #0.0625
                #    offset = [(r - s) // 2 for r, s in zip(self.full_res, size)] 
                #    offset[1] = offset[1] + self.clicky 
                #    self.camera.set_controls({"ScalerCrop": offset + size , "FrameRate": (45)})
                #    self.clickxOld = self.clickx
                #    #print("ZOOMING" + str(self.zoom))    
                #        
                    
                
                
                t_end = time.time()
     
                fps = -1/(t_start - t_end)
                fpsave = fpsave + (fps/30)
                
                
            #fpsave = fpsave/20
            self.fpsaveout = fpsave
            
            
            
            

#def getFrame(obj): 
#    
#        image = thread.imageout
#    
#    
#    return image #send this to the main program 
#


            
thread = CameraThread()
thread.start()

