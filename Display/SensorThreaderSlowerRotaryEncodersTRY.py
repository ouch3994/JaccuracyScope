
import math
from mmc5983_2 import MMC5983
from threading import Thread 
import numpy as np
import board
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
import time 

from adafruit_seesaw import seesaw, rotaryio, digitalio


class SensorThread(Thread): 

    def __init__(self): 
    
        Thread.__init__(self)
        
        
        self.pitch = 0
        self.output_heading = 0
        self.roll = 0
        self.fpsaveout = 0

        
        #initial Sensor Setup! 
        i2c = board.I2C() 
        
        self.accSensor = ISM330DHCX(i2c,0x6b)
        
        #roatry Encoders 
        self.seesaw1 = seesaw.Seesaw(i2c, addr=0x37, reset=True)
        self.seesaw2 = seesaw.Seesaw(i2c, addr=0x36, reset=True)
        
        #seesaw_product = (self.seesaw1.get_version() >> 16) & 0xFFFF
        ##print("Found product {}".format(seesaw_product))
        #if seesaw_product != 4991:
        #    print("Wrong firmware loaded?  Expected 4991")
        #    
        #seesaw_product = (self.seesaw2.get_version() >> 16) & 0xFFFF
        ##print("Found product {}".format(seesaw_product))
        #if seesaw_product != 4991:
        #    print("Wrong firmware loaded?  Expected 4991")   
            
            

        self.seesaw1.pin_mode(24, self.seesaw1.INPUT_PULLUP)
        self.enc1_button = digitalio.DigitalIO(self.seesaw1, 24)
        self.enc1_button_held = False
        
        self.seesaw2.pin_mode(24, self.seesaw2.INPUT_PULLUP)
        self.enc2_button = digitalio.DigitalIO(self.seesaw2, 24)
        self.enc2_button_held = False
        
        
        self.encoder1 = rotaryio.IncrementalEncoder(self.seesaw1)
        self.enc1_last_position = 0
        
        self.encoder2 = rotaryio.IncrementalEncoder(self.seesaw2)
        self.enc2_last_position = 0    

        self.encoder1Output = 0 
        self.encoder2Output = 0 
                    
        ###########end rotarys    
            
            
                
        
        device = "mmc5983"
        
        
        self.mmc = MMC5983(i2cbus=1)
        
        #lastcal = time.time()
        
        frequency = 100
        duration = 200
        stop_on_error = 1
        
        start_time = time.time()
        
        
        #Mag Calibration Area 
        self.declinationAngle = 10-7.85-3;
        #self.degoffset =  108-90; 
        
        self.MafVal = 3
        
        
        self.rollmaker = np.zeros(self.MafVal)
        self.pitchmaker = np.zeros(self.MafVal) 
        self.wobble2xmaker = np.zeros(self.MafVal)     
        self.wobble2ymaker = np.zeros(self.MafVal)  
        self.leadmaker = np.zeros(self.MafVal)
        self.headmaker = 0
        self.compassx =np.zeros(self.MafVal)
        self.compassy =np.zeros(self.MafVal)
        self.compassz =np.zeros(self.MafVal)
        
        self.lead = 0
        self.wobbleY = 0 
        self.wobbleX = 0
        
        self.xoffset = 371.0    #369.00
        self.yoffset = -2326.5  # -2636.00
        self.zoffset = -117.50   #-824.50
                        #
        self.xscale  = 7808.0     #6904.00
        self.yscale  = 7643.50    #7126.00
        self.zscale  = 7807.50     #8376.50
        
        self.cal()
        
        
        
        self.gyrox = 0
        self.gyroy = 0
        self.gyroz = 0
        
        self.gyroFixX  =  0.004734205596034618
        self.gyroFixY  = -0.010995574287564275
        self.gyroFixZ  =  0.0030543261909900766
        
        
        #####CHECK GYRO RANGE  
        self.accSensor.gyro_range = GyroRange.RANGE_125_DPS
        #debug
        #print("GRYO RANGE IS ")
        #print(self.accSensor.gyro_range)        

        
        
        
    def convertToheading(self,rawX,rawY,rawZ):
        #D = math.atan(y/x)*(180/math.pi)
        
        #if (D < 0):
        #   D = D + 360
        
        #return D
        good = True;
       
        normX = (rawX  - self.xoffset)/self.xscale;
        normY = (rawY  - self.yoffset)/self.yscale;
        normZ = (rawZ  - self.zoffset)/self.zscale;
        
        #print(str(rawX) + "  " + str(rawY)+ "   " + str(rawZ)) 
        
        
        heading_r = math.atan2(-normZ,  -normY);
        #heading_r = math.atan2(normY,normZ);
        
        heading_deg = heading_r * (180/math.pi) -  self.declinationAngle + 180;
        
        if(heading_deg < 0 ): 
            heading_deg = heading_deg +360
        
        
        #print(str(heading_deg))
        
        return heading_deg        
        
        
 
    def cal(self):
        self.mmc.calibrate() 
    
    
        
        
    def run(self):
        
        while True: 
            
            #self.val1 = self.val1 +1 

            
            
            #Get a frame : 
            fpsave=0 
                    

                  
            
            #moving Average Filter 
            for i in range (1,self.MafVal+1,1): 
            
            
                t_start = time.time()
                
                try: 
                    self.data = self.mmc.read_data()
                except: 
                    print("Catching Gyro ... lol ")
                    
                #logdata = f"{data.x_raw} {data.y_raw} {data.z_raw} {data.t_raw} {data.x:.6f} {data.y:.6f} {data.z:.6f} {data.t:.3f} {mmc.caldata[0]} {mmc.caldata[1]} {mmc.caldata[2]}"
                
                self.compassx[i-1] = self.data.x_raw
                self.compassy[i-1] = self.data.y_raw
                self.compassz[i-1] = self.data.z_raw 
                
                #self.headmaker = self.convertToheading(self.data.x_raw, self.data.y_raw, self.data.z_raw) #uncalibrated and sucks big cock 
                #print(data.x) #does not workaround zero... 
                
                try: 
                    output_accX = self.accSensor.acceleration[0]
                    output_accY = self.accSensor.acceleration[1]
                    output_accZ = self.accSensor.acceleration[2]
                except: 
                    output_accX = 0
                    output_accY = 0
                    output_accZ = 0
                    
                    
                try:
                    self.gyrox = self.accSensor.gyro[0] - self.gyroFixX
                    self.gyroy = self.accSensor.gyro[1] - self.gyroFixY
                    self.gyroz = self.accSensor.gyro[2] - self.gyroFixZ
                except:
                    print("Catching Gyro ... lol ")
                    self.gyrox = 0
                    self.gyroy = 0
                    self.gyroz = 0
                    
                #print("gyro")
                #print(self.gyrox)
                #print(self.gyroy)
                #print(self.gyroz)
                
                       
                
                self.leadmaker[i-1] = self.gyroy
                self.wobble2xmaker[i-1] = self.gyroz
                self.wobble2ymaker[i-1] = self.gyroy
                self.pitchmaker[i-1] =math.atan2(output_accZ,math.sqrt((output_accY*output_accY)+(output_accX*output_accX)))
                self.rollmaker[i-1] =math.atan2(output_accY,math.sqrt((output_accX*output_accX)+(output_accZ*output_accZ)))
                
                
                #while((time.time() - t_start) < 0.01):
                time.sleep(.01)  #0.01 .016 was a good val just on the accell and shit.  need more  
                
                t_end = time.time()
                fps = -1/(t_start - t_end)
                fpsave = fpsave + (fps/self.MafVal)
                
                #print(output_accZ)
                
                
                
            #fpsave = fpsave/20
            self.fpsaveout = fpsave
            
            # negate the position to make clockwise rotation positive
            try:
                self.enc1_position = -self.encoder1.position
                self.enc2_position = -self.encoder2.position
            except:
                print("Catching... lol ")
                self.enc1_position = 0 
                self.enc2_position = 0 
            

            try:
                if (self.enc1_position != self.enc1_last_position and self.enc1_position < 2147000000):
                    self.encoder1Output = self.enc1_position - self.enc1_last_position 
                    self.enc1_last_position = self.enc1_position
                    #print("enc1_Position: {}".format(self.enc1_position))
                    #print(str(self.encoder1Output))
                
                if not self.enc1_button.value and not self.enc1_button_held:
                    self.enc1_button_held = True
                    #print("enc1_Button pressed")
                
                if self.enc1_button.value and self.enc1_button_held:
                    self.enc1_button_held = False
                    #print("enc1_Button released")                   
                    
                if (self.enc2_position != self.enc2_last_position and self.enc2_position < 2147000000):
                    self.encoder2Output = self.enc2_position - self.enc2_last_position
                    self.enc2_last_position = self.enc2_position
                    #print("enc2_Position: {}".format(self.enc2_position))
                    #print(str(self.encoder2Output))
                
                if not self.enc2_button.value and not self.enc2_button_held:
                    self.enc2_button_held = True
                    #print("enc2_Button pressed")
                
                if self.enc2_button.value and self.enc2_button_held:
                    self.enc2_button_held = False
                    #print("enc2_Button released") 
            except:
                print("Catching BACKEND OF SHIT... lol WTF DUDE ")    
                #self.enc1_button_held = False
                #self.enc2_button_held = False
                
                
                
                
                
                
                
                
                
                
                
                
                
            
            #print(self.pitchmaker)
            self.lead = np.average(self.leadmaker)
            self.pitch = np.average(self.pitchmaker) 
            self.roll  = np.average(self.rollmaker)
            self.wobbleX = np.std(self.wobble2xmaker)*10000#np.std(self.rollmaker)*1000   #make extra 0>> 
            self.wobbleY = np.std(self.wobble2ymaker)*10000#np.std(self.pitchmaker)*1000
            self.output_heading =  self.convertToheading(np.average(self.compassx),np.average(self.compassy),np.average(self.compassx))
            
            
            

#def getFrame(obj): 
#    
#        image = thread.imageout
#    
#    
#    return image #send this to the main program 
#


            
thread = SensorThread()
thread.start()

