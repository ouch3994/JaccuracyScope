import ST7789  
from PIL import Image  
from time import sleep  
import time 
display=ST7789.ST7789(port=0,cs=0,dc=25,backlight=22,spi_speed_hz=99900000)   #dc5 160000000
display._spi.mode=3  
display.reset()  
display._init()  
#image=Image.new('RGB',(240,240),(255,0,0))  #('RGB',(240,240),(r,g,b))
#display.display(image)  
#sleep(2)  

waittimer = 0.04
dingus =1; 
image=Image.open("TestGUI.jpg")  
image=image.resize((240,240),resample=Image.LANCZOS)  
display.display(image, xs =0 ,xe =239 ,ys=0,ye=239)  

image=Image.open("ThermalImage240.jpg") 
image2=Image.open("ThermalImage240red.jpg") 
poop=1
##
while (dingus ==1):
    fpsave =0 
    for i in range (1,20,1):    
    
        t_start = time.time()
        
        
        if (poop == 1 ): 
            display.displayFast(image) 
            poop =0
        else: 
            display.displayFast(image2)
            poop = 1 
        
        
        t_end = time.time()
        fps = -1/(t_start - t_end)
        fpsave = fpsave + fps
    
    
    
    
        
    fpsave = fpsave/20 
    print(fpsave)