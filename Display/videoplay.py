import ST7789  
from PIL import Image  
from time import sleep  
import time 
import cv2 
import os

display=ST7789.ST7789(port=0,cs=0,dc=25,backlight=22,spi_speed_hz=99900000)   #dc5 160000000
display._spi.mode=3  
display.reset()  

display._init()  

waittimer = 0.04
dingus =1; 
image=Image.open("LoadingScreen2.jpg")    
#first diplay, then DiplayFast after this 
display.display(image, xs =0 ,xe =239 ,ys=0,ye=239)  
#display.displayFast(img)

time.sleep(3)
print("Booted")


root = os.getcwd()

# Defaults Params
#videoFile = "Easter240.mp4"
#videoFile = "gametest60.mp4"
videoFile = "VIDEOscope.avi"

frame_step = 1

waitsize = 0.0001




#now video lol 


image_counter = 0
read_counter = 0

print('Read file: {}'.format(videoFile))
cap = cv2.VideoCapture(videoFile) # says we capture an image from a webcam


while(cap.isOpened()):
    ret,cv2_im = cap.read()
    
    t_start = time.time()
    
    if ret and read_counter % frame_step == 0:
    
        converted = cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)
    
        pil_im = Image.fromarray(converted)
        
        time.sleep(waitsize)
    
        display.displayFast(pil_im)
        
        delta = time.time() - t_start
        #if((delta)> 30):
        #    waitsize = delta - 29.97
        #elif ((delta)< 29.9):
        #    waitsize = -(delta - 29.97)
        #
        image_counter += 1
    elif not ret:
        break
        
    #time.sleep(1/30)   
    t_end = time.time()
    fps = -1/(t_start - t_end)
    print(fps)    
    read_counter += 1
             
cap.release()
        
        
print("Finished!")        
