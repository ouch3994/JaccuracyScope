

#addresses are 30 and 6b 

#!/usr/bin/python3
import math 
from mmc5983_2 import MMC5983
import time

import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

i2c = board.I2C() 

accSensor = ISM330DHCX(i2c,0x6b)


device = "mmc5983"


mmc = MMC5983(i2cbus=1)

#lastcal = time.time()

frequency = 100
duration = 200
stop_on_error = 1

start_time = time.time()
declinationAngle = 11.41666666666667;

#cal data Mag 

xoffset = 369.00
yoffset =  -2636.00
zoffset = -824.50

xscale = 6904.00
yscale = 7126.00
zscale = 8376.50




def convertToheading(rawX,rawY,rawZ):
    #D = math.atan(y/x)*(180/math.pi)
    
    #if (D < 0):
     #   D = D + 360
       
    #return D
    good = True;
    
    
    #if (x == 0 or x >= 262143):
    #    good = False;
    #if (y == 0 or y >= 262143):
    #    good = False;
    #if (z == 0 or z >= 262143):
    #    good = False;  
    #
    
    
    #if good: 
    #
    #    #normX = (float(x) - 131072.0)/131072.0;
    #    #normY = (float(y) - 131072.0)/131072.0;
    #    #normZ = (float(z) - 131072.0)/131072.0;
    #    
    #    
    #    if (normY != 0): 
    #        if(normX < 0 ):
    #            if (normY > 0): 
    #                heading  = 57.2958 * math.atan(-normX / normY); # Quadrant 1
    #            else: 
    #                heading = 57.2958 * math.atan(-normX / normY) + 180; # Quadrant 2
    #        else: 
    #            if (normY < 0):
    #                heading = 57.2958 * math.atan(-normX / normY) + 180; # Quadrant 3
    #            else:
    #                heading = 360 - (57.2958 * math.atan(normX / normY)); # Quadrant 4
    #    else: 
    #        if (normX > 0):
    #            heading = 270; 
    #        else: 
    #            heading = 90; 
    #else: 
    #    heading = 999;
    #
   
    normX = (rawX  - xoffset)/xscale;
    normY = (rawY - yoffset)/yscale;
    normZ = (rawZ  - zoffset)/zscale;
   
   
    heading_r = math.atan2(normX, 0- normY);
    #heading_r = math.atan2(normY,normZ);
    
    heading_deg = heading_r * (180/math.pi) +  declinationAngle - 180;
    
    if(heading_deg < 0 ): 
        heading_deg = heading_deg +360
    
    
    
    return heading_deg
    
    
    
    
    
    


def cal():
    mmc.calibrate()
    

#cal()

#while time.time() < start_time + duration:



def getIMUdata(): 

    #if time.time() > lastcal + 60:
     #   cal()
     #   lastcal = time.time()
    data = mmc.read_data()
    #logdata = f"{data.x_raw} {data.y_raw} {data.z_raw} {data.t_raw} {data.x:.6f} {data.y:.6f} {data.z:.6f} {data.t:.3f} {mmc.caldata[0]} {mmc.caldata[1]} {mmc.caldata[2]}"
     
    output_heading = convertToheading(data.x_raw, data.y_raw, data.z_raw) #uncalibrated and sucks big cock 
    #print(data.x)
    
    output_accX = accSensor.acceleration[0]
    output_accY = accSensor.acceleration[1]
    output_accZ = accSensor.acceleration[2]
    
    pitch=-math.atan2(output_accX,math.sqrt((output_accY*output_accY)+(output_accZ*output_accZ)))
    roll =math.atan2(output_accY,math.sqrt((output_accX*output_accX)+(output_accZ*output_accZ)))
    
    #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accSensor.acceleration))
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (accSensor.gyro))
    
    
    #print(output)
    #cal()
     
    return output_heading, pitch, roll 

    #if frequency:
    #    time.sleep(1/frequency)



## Test Code 
#While True: 
#
#   h, p, r = getIMUdata() 
#   
#   #print(h)
#   print(p)
#   #print(r)
#
#   
#   time.sleep(.1)
#   