from PIL import Image
from PIL import ImageFont 
from PIL import ImageDraw
from PIL import ImageChops

import numpy as np
import math





#yardsTest = np.array([0, 10, 20, 30, 40,  50, 60 ])
#inchesTest = np.array([-0.8, -5.1, -15.2, -40, -59.0, -65, -80 ])


graph=Image.open("plotbase.jpg")
rawgraph=Image.open("plotbase.jpg")
draw2 = ImageDraw.Draw(graph)



graph2=Image.open("lobstermodebase2.jpg")
rawgraph2=Image.open("lobstermodebase2.jpg")
draw2lo = ImageDraw.Draw(graph2)


#rawgraph = Image.open("plotbase.jpg")

def trajPlotter(distanceData, dropData,dist_targ): 

    #outputy = np.zeros(len(dropData))
                
    #outputx = np.zeros((1,len(dropData[:]))
 
    outputy = elev2Y(dropData)
    outputx = range2x(distanceData,dist_targ)
     
    return outputy, outputx 
    
     
def elev2Y(inches):
  
    plotHeightpx = 25; 
    pxoffset  = 2; 
      
    pxunits= (np.max(inches) - np.min(inches)) / plotHeightpx; 
    h_max = np.max(inches) ;
    
    
    youtput = np.zeros(len(inches));
    
    for i in range(len(inches)):
        youtput[i] = -(((inches[i])-h_max) / pxunits)    +  pxoffset ;
        
    return youtput
    
    
def range2x(yards,dist_targ):
  
    plotWidthpx = 100; 
    pxoffset  = 5+1; 
      
    h_max = np.max(yards) ;
    
    
    #if(dist_targ >= 1100 and dist_targ < 3000):
    #    divider = 1500; 
    #elif(dist_targ >= 505 and dist_targ < 1100):
    #    divider = 1000;
    #elif(dist_targ >= 255 and dist_targ < 505):
    #    divider = 500;
    #elif(dist_targ >= 0 and dist_targ < 255):
    #    divider = 250;
    
    
    
    xoutput = np.zeros(len(yards));
    
    for i in range(len(yards)):
        xoutput[i] = ((yards[i]) / dist_targ  ) * plotWidthpx    +  pxoffset ; ## was /1000 or /dividier for even scaling 
        
    return xoutput  
    
    
    
    #LOB MODE PLOTTER 
def trajPlotter2(distanceData, dropData,dist_targ): 

    #outputy = np.zeros(len(dropData))
                
    #outputx = np.zeros((1,len(dropData[:]))
 
    outputy = elev2Y2(dropData)
    outputx = range2x2(distanceData,dist_targ)
     
    return outputy, outputx 
    
    
def elev2Y2(inches):
  
    plotHeightpx = 180; 
    pxoffset  = 2; 
      
    pxunits= (np.max(inches) - np.min(inches)) / plotHeightpx; 
    h_max = np.max(inches) ;
    
    
    youtput = np.zeros(len(inches));
    
    for i in range(len(inches)):
        youtput[i] = -(((inches[i])-h_max) / pxunits)    +  pxoffset ;
        
    return youtput
    
    
def range2x2(yards,dist_targ):
  
    plotWidthpx = 240; 
    pxoffset  = 9; 
      
    h_max = np.max(yards) ;
    
    
    #if(dist_targ >= 1100 and dist_targ < 3000):
    #    divider = 1500; 
    #elif(dist_targ >= 505 and dist_targ < 1100):
    #    divider = 1000;
    #elif(dist_targ >= 255 and dist_targ < 505):
    #    divider = 500;
    #elif(dist_targ >= 0 and dist_targ < 255):
    #    divider = 250;
    
    
    
    xoutput = np.zeros(len(yards));
    
    for i in range(len(yards)):
        xoutput[i] = ((yards[i]) / 3000  ) * plotWidthpx    +  pxoffset ; ## was /1000 or /dividier for even scaling 
        
    return xoutput  


    
    
    


## Test the coding: 
 
def plotme(yards,inches,dist_targ, mode):   #plot up to this distance
    
    if (mode==0):
        y, x = trajPlotter(yards, inches,dist_targ)
        
        
        
        #Image.new('RGB',(150,30),(0,0,0))
        #image.show()
        
        
        
        graph.paste(rawgraph,(0,0))
       
    
    
        #print(max(x))
        #draw2.rectangle((6, 0 , 94, 180), (0,0,0))
        for i in range(len(x)-1):
            draw2.point((x[i],y[i]),(0,120,255))
            #draw2.point((x[i],y[i]+1),(0,120,255)) #makes the image wider lolz
        #graph.show() 
        return graph
        
    elif (mode==1):
    
    
        y, x = trajPlotter2(yards, inches,dist_targ)

        graph2.paste(rawgraph2,(0,0))
        
        #print(max(x))
        #draw2lo.rectangle((9, 0, 239, 177), (0,0,0))  #177
        for i in range(len(x)-1):
            draw2lo.point((x[i],y[i]+30),(0,120,255))
            #draw2.point((x[i],y[i]+1),(0,120,255)) #makes the image wider lolz
            draw2lo.point((x[i],y[i]-1+30),(0,120,255)) #makes the image wider lolz
            draw2lo.point((x[i]+1,y[i]+30),(0,120,255))
            draw2lo.point((x[i]-1,y[i]+30),(0,120,255))
        #graph.show() 
        

        

        
        
        
        
        
        return graph2
    
    
    
