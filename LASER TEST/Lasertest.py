

import time 
import serial
import struct

ser = serial.Serial('/dev/ttyS0',9600,timeout = 2)  # open serial port  #TIMEOUT timeout=1 ?
print(ser.name)         # check which port was really used  ttyS0 serial0



#commands: 

#######Single Ranger:  

# Send Command:  AEA704000509BCBE
#OR     "\xAE\xA7\x04\x00\x05\x09\xBC\xBE"
cmdsingle = [0xAE,0xA7,0x04,0x00,0x05,0x09,0xBC,0xBE]

######Continuous lol 
 #Start  Command:  AEA704000E12BCBE
 #      "\xAE\xA7\x04\x00\x0E\x12\xBC\xBE"
 
 #End Command:  AEA704000F13BCBE
 
  #  "\xAE\xA7\x04\x00\x0F\x13\xBC\xBE"
 
 
#failed response is same as command AEA704000509BCBE
#good response is 
#0xAE 0xA7 0x17 0x00 0x85 (0xDATA x 19)  0xBC 0xBE

#DATA FORMAT (each 2 bytes) 
#Elevation,  Straight distance,  sine height,  
#horiz distance,  twopoints high,  aximuth,   
#horix anlgge,  span,  speed, 
#distance unit, elevaiton

#sample in room:  
#AE A7 17 00 85 data/ 00 00 00 27 00 00 00 27 00 00 00 
#00 00 00 00 00 00 00 01 EB \data BC BE 

#distance:  00 27   or 39d
#units: 0.1 meters 
#is 3.9meters 


#need to extract the bytes; 8 and 9   or 7&8 (index0)  distance
#24 or 23 index 0  for units... 0.1 meters.. 


while (True):

    #input("Press Enter to take Measurement: ")


    #print("Commanding Single Read...")
    ser.write(serial.to_bytes(cmdsingle))  
    time.sleep(1)
    response = ser.read(27)
    
    print("Raw Response:")
    print (response.hex())
    
    recieved_data_length = len(response)
    

    
    if (recieved_data_length>8):
        
        #print("Converted")
        trythis = int.from_bytes(response[7:9],"big")
        #print (trythis)
        #print (type(trythis))
        outputdata = float(trythis) * 0.1 * 1.09361; #yards now 
        
        print( "Distance measured: " + str(outputdata) + " yards" )
        
        
    else:
        print("Measrement Failed.")
        outputdata = 0; 
    
    #print("Sleeping ... ")
    
    time.sleep(2)

  
